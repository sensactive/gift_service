from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

_MAX_SIZE = 300


# Create your models here.
class GiftUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars/%Y/%m/%d', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True, blank=True, default=18)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

        # Функция ограничения размера аватарки

    def save(self, *args, **kwargs):
        # Сначала - обычное сохранение
        super(GiftUser, self).save(*args, **kwargs)

        # Проверяем, указан ли аватар
        if self.avatar:
            filename = self.avatar.path
            width = self.avatar.width
            height = self.avatar.height

            max_size = max(width, height)

            # Может, и не надо ничего менять?
            if max_size > _MAX_SIZE:
                # Надо, Федя, надо
                image = Image.open(filename)
                # resize - безопасная функция, она создаёт новый объект, а не
                # вносит изменения в исходный, поэтому так
                image = image.resize(
                    (round(width / max_size * _MAX_SIZE),  # Сохраняем пропорции
                     round(height / max_size * _MAX_SIZE)),
                    Image.ANTIALIAS
                )
                # И не забыть сохраниться
                image.save()


class GiftUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(GiftUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=GiftUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            GiftUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=GiftUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.giftuserprofile.save()
