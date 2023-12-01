from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
SOCIAL_MEDIA_TYPE = (
    ('instagram', 'instagram'), ('facebook', 'facebook'),
    ('linkedin', 'linkedin'), ('youtube', 'youtube'),
    ('twitter', 'twitter'), ('telegram', 'telegram'), ('skype', 'skype')
)

GENDER = (
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other')
)

MARITAL_STATUS = (
    ('single', 'single'), ('married', 'married'),
    ('widowed', 'widowed'), ('divorced', 'divorced'),
    ('separated', 'separated')
)

BLOOD_GROUP_CHOICES = (
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-')
)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    blood_group = models.CharField(max_length=255, choices=BLOOD_GROUP_CHOICES, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=255, choices=MARITAL_STATUS, null=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='static/images', null=True, blank=True)

    def __str__(self):
        return self.user


class Service(models.Model):
    title = models.CharField(max_length=150, blank=False, unique=True)
    description = models.CharField(max_length=512, blank=False, unique=True)
    icon = models.FileField(upload_to='static/images', validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)], default="")


class ContactForm(models.Model):
    name = models.CharField(max_length=20, help_text='required')
    email = models.EmailField(max_length=100, help_text='required')
    subject = models.CharField(max_length=30)
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.email


class feedback(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, help_text='required')
    rating = models.CharField(max_length=10)
    message = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class CompanyLogo(models.Model):
    logo = models.FileField(upload_to='static/images', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
                            default="")


class Banner(models.Model):
    title = models.CharField(max_length=150, blank=False, unique=True)
    description = models.CharField(max_length=512, blank=False, unique=True)
    icon = models.FileField(upload_to='static/images', validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)], default="")


class Technology(models.Model):
    title = models.CharField(max_length=150, blank=False, unique=True)
    icon = models.FileField(upload_to='static/images', validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)], default="")


class Template(models.Model):
    title = models.CharField(max_length=150, blank=False, unique=True)
    image = models.FileField(upload_to='static/images', validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)], default="")
    link = models.URLField(max_length=255, default=None)
    price = models.FloatField(null=True, blank=True)


class Notice(models.Model):
    title = models.CharField(max_length=150, blank=False, unique=True)
    date = models.DateTimeField(null=True, blank=True)
    image = models.FileField(upload_to='static/images', default="")


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.CharField(max_length=20, null=True, blank=True)
    items = models.JSONField(default=dict)
    total = models.FloatField(default=None, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_approve = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=30, default=None)
    email = models.EmailField(blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=13, blank=False, default=None)
    address = models.CharField(max_length=150, default=" ")
    delivery_instruction = models.CharField(max_length=250, blank=True, null=True)
    deliver_date = models.DateField(null=True, blank=True)
    is_deliver = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.order_id

    @classmethod
    def send_mail(cls, sender, context):
        pass


class GlobalLocation(models.Model):
    email = models.EmailField(max_length=255, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)


class SocialMedia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    typ = models.CharField(max_length=255, choices=SOCIAL_MEDIA_TYPE, null=True, blank=True)
    icon = models.FileField(upload_to='static/images', validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)], default="")
    link = models.URLField(max_length=255, null=True, blank=True)


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
