from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()

    if not User.objects.filter(username='ulukata-admin').exists():
        User.objects.create_superuser(
            username='ulukata-admin',
            email='admin@example.com',
            password='445415Admin'
        )