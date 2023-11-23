import os
import pkg_resources

from django.core.management import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name = options.pop("name")

        self._create_app(
            app_name=app_name,
            template_name="app_template",
            **options,
        )

    def _create_app(self, app_name, template_name, **options):
        if os.path.exists('app'):
            target = f"app/{app_name}"
        else:
            target = app_name
        top_dir = os.path.abspath(os.path.expanduser(target))
        try:
            self._make_dirs(top_dir)
            template_path = pkg_resources.resource_filename(
                "drf_plus", os.path.join("management", template_name)
            )
            options["template"] = "file://" + str(template_path)
            super().handle("app", app_name, target, **options)
        except CommandError as e:
            print(e)
            self.stderr.write(f'"{app_name}" 생성간 오류가 발생했습니다.\n=> {e}')

    @staticmethod
    def _make_dirs(top_dir):
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            raise CommandError("'%s' already exists" % top_dir)
        except OSError as e:
            raise CommandError(e)
