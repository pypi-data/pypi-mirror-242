from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    pass


class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    recipient_email = models.EmailField(_("Email address"), unique=True)
    token = models.CharField(max_length=32, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Invitation: '{self.recipient_email}'>"

    def save(self, *args, **kwargs):
        adding = self._state.adding
        if adding:
            self.token = get_random_string(
                length=self._meta.get_field("token").max_length
            )
        super().save(*args, **kwargs)
        if adding:
            self.send()

    @property
    def subject(self):
        return f"{self.sender.username} invited you to join"

    def send(self):
        server_host = getattr(settings, "SERVER_HOST", "127.0.0.1")
        server_port = getattr(settings, "SERVER_PORT", 8080)
        termination = getattr(settings, "SERVER_TLS_TERMINATION", False)

        scheme = "https" if termination else "http"
        host = (
            server_host
            if server_port == 80
            else ":".join((server_host, str(server_port)))
        )

        context = {"invitation": self, "server_address": f"{scheme}://{host}"}
        html = render_to_string("hub/emails/invitation.j2", context)
        txt = render_to_string("hub/emails/invitation.txt", context)

        email = EmailMultiAlternatives(
            self.subject, txt, settings.DEFAULT_FROM_EMAIL, [self.recipient_email]
        )
        email.attach_alternative(html, "text/html")
        email.send()
