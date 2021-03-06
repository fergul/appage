from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    app_tracker_id = models.CharField(_('app tracker id'), max_length=30, blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)
    
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class Device(models.Model):
    TYPE_CHOICES = (('NA','What am I?'),
                    ('MOB', 'Mobile'),
                    ('TAB', 'Tablet'),
                    ('PC', 'Computer'))

    owner = models.ForeignKey('User')
    device_id = models.CharField(max_length=500)
    device_name = models.CharField(max_length=50)
    device_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    user = models.CharField(max_length=50)
    last_checked = models.CharField(max_length=50)


class Application(models.Model):
    device = models.ForeignKey('Device')
    appname = models.CharField(max_length=100)
    total_time = models.IntegerField()

class Session(models.Model):
    dev_app = models.ForeignKey('Application')
    time_spent = models.IntegerField()
    time_stamp = models.IntegerField()

class Notification(models.Model):
    time_stamp = models.IntegerField() 
    device = models.ForeignKey('Device')
    session = models.ForeignKey('Session')
# applications = {'facebook':{'total':23232323232, 'sessions':[ {'startTime':23232322323,'length':223232}, {'startTime':23232322323,'length':223232}],
#                 'snapchat':{'total':23232323232, 'sessions':[ {'startTime':23232322323,'length':223232}, {'startTime':23232322323,'length':223232}],
#                 }