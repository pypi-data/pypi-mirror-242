from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application
import gunicorn.app.base
import multiprocessing

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django.conf import settings


class WSGIServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class Command(BaseCommand):
    help = "Run Gunicorn server"

    def add_arguments(self, parser):
        parser.add_argument("--host", help="The host to listen on")
        parser.add_argument("--port", help="The port to listen on")
        parser.add_argument("--workers", help="Number of workers")

    def handle(self, *args, **options):
        settings.SERVER_HOST = options["host"] or getattr(
            settings, "SERVER_HOST", "127.0.0.1"
        )
        settings.SERVER_PORT = options["port"] or getattr(settings, "SERVER_PORT", 8080)

        application = (
            StaticFilesHandler(get_wsgi_application())
            if settings.DEBUG
            else get_wsgi_application()
        )

        server_options = {
            "bind": "{}:{}".format(settings.SERVER_HOST, settings.SERVER_PORT),
            "workers": options["workers"] or (multiprocessing.cpu_count() * 2) + 1,
        }
        WSGIServer(application, options=server_options).run()
