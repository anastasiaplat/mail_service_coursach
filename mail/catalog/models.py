from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile.png", null=True, upload_to='profile_pics/', verbose_name='Аватар ')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения ')
    telephone = models.CharField(max_length=11,blank=True, null=True, verbose_name='Телефон')
    location = models.CharField(max_length=100,blank=True, null=True, verbose_name='Местоположение')
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

class Letter(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='output')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='input',
                                verbose_name="Кому")
    theme = models.CharField(max_length=200, verbose_name="Тема", null=True)
    content = models.TextField(verbose_name="Содержание")
    date_sended = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_sended']

    def __str__(self):
        return str(self.author)

    def get_absolute_url(self):
        return reverse('letter_detail', args=[str(self.id)])
