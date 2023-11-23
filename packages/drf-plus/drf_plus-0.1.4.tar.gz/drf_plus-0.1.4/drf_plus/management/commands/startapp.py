import os

from django.conf import settings
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
        # 'app' 폴더가 있는지 확인하고 경로 설정
        if os.path.exists('app'):
            target = f"app/{app_name}"
        else:
            target = app_name

        top_dir = os.path.abspath(os.path.expanduser(target))

        try:
            self._make_dirs(top_dir)
            # 템플릿 경로는 drf_plus 라이브러리의 app_template 폴더를 가리키도록 설정
            options["template"] = "file://" + str(
                settings.BASE_DIR / "drf_plus" / "management" / "app_template"
            )
            super().handle("app", app_name, target, **options)
        except CommandError as e:
            print(e)
            self.stderr.write(f'"{app_name}" app already exists.')

    @staticmethod
    def _make_dirs(top_dir):
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            raise CommandError("'%s' already exists" % top_dir)
        except OSError as e:
            raise CommandError(e)
