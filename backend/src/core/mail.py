import smtplib
from typing import cast

from flask import Flask

mail = smtplib.SMTP()


def init(app: Flask):
    host = cast(str, app.config.get("SMTP_HOST"))  # pyright: ignore[reportUnknownMemberType]
    port = cast(int, app.config.get("SMTP_PORT"))  # pyright: ignore[reportUnknownMemberType]
    login = cast(str, app.config.get("SMTP_LOGIN"))  # pyright: ignore[reportUnknownMemberType]
    password = cast(str, app.config.get("SMTP_PASSWORD"))  # pyright: ignore[reportUnknownMemberType]
    _ = mail.connect(host, port)
    _ = mail.starttls()
    _ = mail.login(login, password)
    config(app)


def config(app: Flask):
    """
    Configures the SMTP session teardown.
    """

    @app.teardown_request
    def close_smtp_session(exception: BaseException | None = None):  # pyright: ignore[reportUnusedFunction]
        app.logger.exception(exception)
        app.logger.info(mail.quit())
