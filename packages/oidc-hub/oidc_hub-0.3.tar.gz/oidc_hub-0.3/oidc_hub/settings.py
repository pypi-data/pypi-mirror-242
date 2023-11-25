from django.conf import settings

settings.SERVER_HOST = getattr(settings, "SERVER_HOST", "127.0.0.1")
settings.SERVER_PORT = getattr(settings, "SERVER_PORT", 8080)
settings.SERVER_TLS_TERMINATION = getattr(settings, "SERVER_TLS_TERMINATION", False)

# enforce SERVER_HOST presence in ALLOWED_HOSTS list
# https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
if settings.SERVER_HOST not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append(settings.SERVER_HOST)
