from django.core.management.base import BaseCommand
from .fill_users import fill as fill_user
from ...models import User



class Command(BaseCommand):
    help = 'Заполнение базы данных'


    def handle(self, *args, **options):

        _ = User.objects.create_superuser(
            username='admin', email='admin@localhost', password='admin'
        )
        fill_user()
