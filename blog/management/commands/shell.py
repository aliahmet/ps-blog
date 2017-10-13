from IPython import embed
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.termcolors import colorize
from traitlets.config import get_config
from django.utils import timezone
from django.db.models import F, Aggregate, Count, Q, Avg, Sum
from django.conf import settings, global_settings
class Command(BaseCommand):
    help = 'Super Django Shell'

    def custom_commands(self):
        pass

    def handle(self, *args, **options):
        User = get_user_model()
        helpers = [
            ("Date", "datetime, timedelta, time"),
            ("django.utils", "timezone, termcolors, dateformat, translation."),
            ("django.conf", "settings"),
            ("%quickref", "Quick reference."),
            ("User", "Django Auth Model"),
            ("help", "Python's own help system."),
            ("object?", "Details about 'object'"),
            ("object??", "More Details about 'object' "),
        ]
        registered_models = {}
        for model in apps.get_models():
            module = model.__module__
            name = model.__name__
            locals()[name] = model
            try:
                registered_models[module].append(name)
            except:
                registered_models[module] = [name]

        for module in registered_models:
            helpers.append((module, ", ".join(registered_models[module])))

        banner2 = "\n".join(
                ["%s: %s" % (colorize(x, fg="yellow"), y) for x, y in
                 helpers]) + "\n" + colorize("RELOAD: \n %load_ext autoreload \n %autoreload", fg="red") + "\n"
        banner = "Hi! \n\n" \
                 "Here some useful shortcuts (Crtl-D to exit):"

        c = get_config()

        c.InteractiveShell.banner1 = banner
        c.InteractiveShell.banner2 = banner2
        c.TerminalInteractiveShell.confirm_exit = False
        c.InteractiveShellApp.extensions = ['autoreload']
        c.InteractiveShellApp.exec_lines = ['%autoreload 2', 'print 1asd']
        rtx = embed(config=c)
