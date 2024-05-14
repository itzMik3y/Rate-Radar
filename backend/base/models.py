from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from decimal import Decimal
# Custom User Manager
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Password is not provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id, filename)

# User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_subscribed = models.BooleanField(default=False)
    time_zone = models.CharField(max_length=50, default='UTC')
    preferred_currency = models.CharField(max_length=3, default='USD')
    language = models.CharField(max_length=10, default='en')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='base_currency_subscriptions')
    target_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='target_currency_subscriptions')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'base_currency', 'target_currency')

    def __str__(self):
        return f"{self.user.email} - {self.base_currency.code} to {self.target_currency.code}"

class NotificationCondition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_conditions')
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='condition_base_currency')
    target_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='condition_target_currency')
    threshold_value = models.DecimalField(max_digits=10, decimal_places=2)
    direction = models.CharField(max_length=10, choices=(('GT', 'Greater Than'), ('LT', 'Less Than')))  # GT for greater than, LT for less than
    triggered = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'base_currency', 'target_currency', 'threshold_value', 'direction')

    def __str__(self):
        return (f"{self.user.email} - {self.base_currency.code}/{self.target_currency.code} " 
                f"{self.direction} {self.threshold_value}")
