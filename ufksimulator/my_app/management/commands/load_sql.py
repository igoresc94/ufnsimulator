from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Load initial SQL data'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(base_dir, 'data', 'eu_fake_news_db_with_data.sql')
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql_script)

        self.stdout.write(self.style.SUCCESS('SQL file loaded successfully!'))
