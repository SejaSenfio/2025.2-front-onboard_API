import os
import traceback

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand

from config.settings import DJANGO_SETT


class Command(BaseCommand):
    help = "Executa automaticamente todos os comandos de popular banco de dados de todos os apps"

    def handle(self, *args: list, **kwargs: dict) -> None:
        if not DJANGO_SETT.DEBUG:
            self.stdout.write(
                self.style.WARNING(
                    "Este comando só pode ser executado em ambiente de desenvolvimento!"
                )
            )
            return None

        commands = []

        for app_config in apps.get_app_configs():
            management_path = os.path.join(app_config.path, "management/commands")
            if os.path.exists(management_path):
                for file in os.listdir(management_path):
                    if file.startswith("devsetup_") and file.endswith(".py"):
                        cmd_name = file.replace(".py", "")
                        commands.append(cmd_name)

        if not commands:
            self.stdout.write(self.style.WARNING("Nenhum comando de popularização encontrado."))
            return

        for cmd in sorted(commands):
            self.stdout.write(self.style.NOTICE(f"Executando {cmd}..."))
            try:
                call_command(cmd)
                self.stdout.write(self.style.SUCCESS(f"{cmd} executado com sucesso!"))
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f"Erro ao executar {cmd}: {e} {''.join(traceback.format_exception(None, e, e.__traceback__))}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Todos os dados foram populados com sucesso!"))
