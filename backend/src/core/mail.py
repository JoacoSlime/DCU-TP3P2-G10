from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import (
    SMTP,
    SMTPServerDisconnected,
)
from typing import cast

from flask import Flask


class MailHandler:
    def __init__(self):
        self.initialized: bool = False
        self.host: str = ""
        self.port: int = 0
        self.login: str = ""
        self.password: str = ""
        self.sender: str = ""
        self.url: str | None = ""
        self.client: SMTP = SMTP()

    def init(self, app: Flask):
        self.initialized = True
        self.host = cast(str, app.config.get("SMTP_HOST"))  # pyright: ignore[reportUnknownMemberType]
        self.port = cast(int, app.config.get("SMTP_PORT"))  # pyright: ignore[reportUnknownMemberType]
        self.login = cast(str, app.config.get("SMTP_LOGIN"))  # pyright: ignore[reportUnknownMemberType]
        self.password = cast(str, app.config.get("SMTP_PASSWORD"))  # pyright: ignore[reportUnknownMemberType]
        self.sender = cast(str, app.config.get("SMTP_SENDER_EMAIL"))  # pyright: ignore[reportUnknownMemberType]
        self.url = cast(str, app.config.get("URL_BASE_PUBLIC_APP"))  # pyright: ignore[reportUnknownMemberType]

    def send_verification_mail(self, receiver: str, token: str) -> None:
        if not self.initialized:
            raise RuntimeError("MailHandler must be initialized before use")
        message = MIMEMultipart()
        message["To"] = receiver
        message["From"] = self.sender
        message["Subject"] = "Invitación a colaborar en ContaminApp"
        body = f"""\
    <h1>Fuiste invitade a ContaminApp</h1>

    <p>Para finalizar la creación de tu cuenta, crea tu contraseña <a href="{self.url if self.url else "http://localhost:5000"}/finalizar_registro?token={token}">aquí</a></p>

    <p>O copia este enlace: {self.url if self.url else "http://localhost:5000"}/finalizar_registro?token={token}</p>"""
        message.attach(MIMEText(body, "html"))

        _ = self.client.connect(self.host, self.port)
        _ = self.client.starttls()
        _ = self.client.login(self.login, self.password)
        _ = self.client.sendmail(self.sender, receiver, message.as_string())
        _ = self.client.quit()

    def teardown(self):
        if not self.initialized:
            return None
        try:
            return self.client.quit()
        except SMTPServerDisconnected:
            return None



mail_handler = MailHandler()

def init(app: Flask):
    mail_handler.init(app)
    config(app)

def config(app: Flask):
    """
    Configures the SMTP session teardown.
    """

    @app.teardown_request
    def close_smtp_session(exception: BaseException | None = None):  # pyright: ignore[reportUnusedFunction]
        if exception:
            app.logger.exception(exception)
        app.logger.info(mail_handler.teardown())
