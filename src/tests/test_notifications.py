# tests/test_notifications.py

import pytest
from utils.notifications import Notification

def test_send_email(mocker):
    # Mock SMTP de yagmail
    mock_smtp = mocker.patch("utils.notifications.yagmail.SMTP")
    mock_yag = mock_smtp.return_value

    notification = Notification("destinatario@correo.com")
    content = "Esto es una prueba"

    notification.send_email(content)

    mock_yag.send.assert_called_once_with(
        to="destinatario@correo.com",
        subject=notification._default_title,
        contents=content
    )

def test_message_subida_bajada(mocker):
    mocker.patch("utils.notifications.yagmail.SMTP")

    notification = Notification("dest@correo.com")

    assert "SUBIDO" in notification.messages("subida")
    assert "BAJADO" in notification.messages("bajada")
