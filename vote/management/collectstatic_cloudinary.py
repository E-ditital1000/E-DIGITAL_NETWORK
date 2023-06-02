import os
from django.conf import settings
from django.core.management.base import BaseCommand
import cloudinary.uploader

class Command(BaseCommand):
    help = 'Collect static files and upload them to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument('--unhashed', action='store_true', help='Upload files as unhashed')

    def handle(self, *args, **options):
        # Collect static files to the configured STATIC_ROOT
        self.stdout.write(self.style.SUCCESS('Collecting static files...'))
        self._collect_static()

        # Upload static files to Cloudinary
        self.stdout.write(self.style.SUCCESS('Uploading static files to Cloudinary...'))
        self._upload_static_files(options['unhashed'])

        self.stdout.write(self.style.SUCCESS('Static files upload complete.'))

    def _collect_static(self):
        from django.core.management.commands.collectstatic import Command as CollectStaticCommand

        collect_static_command = CollectStaticCommand()
        collect_static_command.execute()

    def _upload_static_files(self, unhashed):
        for root, dirs, files in os.walk(settings.STATIC_ROOT):
            for file in files:
                file_path = os.path.join(root, file)
                if unhashed:
                    filename = file
                else:
                    filename = file.split('/')[-1]  # Extract the filename without the directory structure
                cloudinary.uploader.upload(file_path, public_id=filename, folder='your_folder_name')
                self.stdout.write(self.style.SUCCESS(f'Uploaded: {file_path}'))
