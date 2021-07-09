from django.core.management.base import BaseCommand
from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):

        users = ShopUser.objects.all()
        for user in users:
            if not ShopUserProfile.objects.filter(user=user):
                user_profile = ShopUserProfile.objects.create(user=user)
                user_profile.save()