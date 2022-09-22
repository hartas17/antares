import os
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = 'Renames a Django project'

    def add_arguments(self, parser):
        parser.add_argument('new_project_name', type=str, help='The new Django project name')

    def handle(self, *args, **kwargs):
        new_project_name = kwargs['new_project_name']

        # Logica para renombrar los archivos
        files_to_rename = ['boilerplate/settings/base.py', 'boilerplate/wsgi.py', 'manage.py']
        folder_to_rename = 'boilerplate'

        for f in files_to_rename:
            with open(f, 'r') as file:
                filedata = file.read()

                # Cada que se renombra un proyecto se genera una nueva secret key
                if file.name == 'boilerplate/settings/base.py':
                    new_key = get_random_secret_key()
                    filedata = filedata.replace('q#4ot4302m^yx2$v$dhant-bjo7nl#b)jhhppe2hb#m@77x6g$', new_key)

            filedata = filedata.replace('boilerplate', new_project_name)

            with open(f, 'w') as file:
                file.write(filedata)

        os.rename(folder_to_rename, new_project_name)
        os.makedirs(f'{new_project_name}/media')

        self.stdout.write(self.style.SUCCESS(f'Project has been renamed to {new_project_name}'))
