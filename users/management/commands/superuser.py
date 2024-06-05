from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='tanyusha_tokor@mail.ru',
            first_name='tatianat',
            last_name='Home',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('nfyz2013')
        user.save()
