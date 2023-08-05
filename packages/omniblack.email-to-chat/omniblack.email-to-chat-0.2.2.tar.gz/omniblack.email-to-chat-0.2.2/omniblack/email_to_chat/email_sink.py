import ssl
from email import message_from_string, message_from_bytes
from email.message import EmailMessage
from email.policy import SMTPUTF8, strict
from email.utils import parseaddr
from yarl import URL
from asyncio import create_task, get_running_loop
from logging import getLogger

from aiosmtpd.smtp import SMTP
from aiosmtpd.handlers import AsyncMessage

from omniblack.systemd import get_sockets_from_fds

from . import __pkg_name__
from .model import InputSink, MessageType, Message

log = getLogger(__name__)

COMMASPACE = ', '


def create_message(email: EmailMessage):
    from_addr = email['From']
    program, addr = parseaddr(from_addr)
    url = URL(f'mailto://{addr}')
    if not program:
        if url.user:
            program = url.user
        else:
            program = url.host

    host = url.host
    type = getattr(MessageType, email.get('X-type', 'report'))
    user, addr = parseaddr(email['To'])
    if not user:
        url = URL(f'mailto://{addr}')
        if url.user:
            user = url.user
        else:
            user = url.host

    body = email.get_content()

    return Message(
        type=type,
        program=program,
        host=host,
        user=user,
        body=body,
    )


class ChatHandler(AsyncMessage):
    def __init__(
            self,
            *args,
            queue,
            message_class=None,
            policy=None,
            **kwargs,
    ):
        if message_class is None:
            message_class = EmailMessage

        if policy is None:
            policy = SMTPUTF8 + strict

        super().__init__(*args, message_class=message_class, **kwargs)
        self.policy = policy
        self.queue = queue

    async def handle_message(self, message):
        create_task(self.queue.put(message))

    def prepare_message(self, session, envelope):
        # If the server was created with decode_data True, then data will be a
        # str, otherwise it will be bytes.
        data = envelope.content
        if isinstance(data, bytes):
            message = message_from_bytes(
                data,
                self.message_class,
                policy=self.policy,
            )
        else:
            assert isinstance(data, str), (
                f'Expected str or bytes, got {type(data)}'
            )
            message = message_from_string(
                data,
                self.message_class,
                policy=self.policy,
            )
            message['X-Peer'] = str(session.peer)
            message['X-MailFrom'] = envelope.mail_from
            message['X-RcptTo'] = COMMASPACE.join(envelope.rcpt_tos)
        return create_message(message)


class Email(InputSink):
    def __init__(
        self,
        *,
        enable_SMTPUTF8=None,
        ssl_context: ssl.SSLContext = None,
        server_kwargs=None,
    ):
        super().__init__()
        self.smtpd = None
        self.server = None
        self.ssl_context = ssl_context
        self.loop = get_running_loop()
        self.server_kwargs = server_kwargs or {}
        self.handler = ChatHandler(queue=self.queue)

        sockets = get_sockets_from_fds()
        self.socket = sockets[f'{__pkg_name__}.socket'][0]

    def factory(self):
        """Allow subclasses to customize the handler/server creation."""
        return SMTP(
            self.handler, **self.server_kwargs
        )

    def _factory_invoker(self):
        """Wraps factory() to catch exceptions during instantiation"""
        self.smtpd = self.factory()
        if self.smtpd is None:
            raise RuntimeError("factory() returned None")
        return self.smtpd

    async def start(self):
        log.info('Starting Email Server')
        self.server = await self.loop.create_server(
            self._factory_invoker,
            sock=self.socket,
            ssl=self.ssl_context,
        )

        log.info('Server started')

    async def stop(self):
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()
