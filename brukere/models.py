from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profilbilder')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} profil'

    def save(self):
        super().save() #<-- kjører save fra parent, så vi ikke mister noe funksjonalitet

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

