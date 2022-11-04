from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomModelManager(CustomUserManager):
    pass