import os

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from SU_Transportation import settings


UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def send_greetings_email(sender, instance, created, **kwargs):
    if created:
        subject = 'SU Transportation Inc.'
        html_message = render_to_string('greeting.html', {'user': instance})
        plain_message = strip_tags(html_message)
        to = instance.email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to],
            html_message=html_message
        )


@receiver(post_delete, sender=UserModel)
def delete_related_file(sender, instance, **kwargs):
    if instance.profile_picture:
        file_path = instance.profile_picture.path
        if os.path.exists(file_path):
            os.remove(file_path)


@receiver(pre_save, sender=UserModel)
def pre_save_image(sender, instance, *args, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).profile_picture.path
        try:
            new_img = instance.profile_picture.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass