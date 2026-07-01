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
