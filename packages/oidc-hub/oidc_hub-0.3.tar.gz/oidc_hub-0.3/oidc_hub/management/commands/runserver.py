from django.conf import settings
from django.core.management.commands import runserver


class Command(runserver.Command):
    """
    This class overrides the addrport from the `runserver` command to use settings
    SERVER_HOST:SERVER_PORT as a default in case `addrport` argument was not
    specified at the command-line
    """

    def handle(self, *args, **options):
        if not options["addrport"]:
            try:
                host = getattr(settings, "SERVER_HOST")
                port = getattr(settings, "SERVER_PORT")
                options["addrport"] = f"{host}:{port}"
            except:
                pass
        super().handle(*args, **options)
