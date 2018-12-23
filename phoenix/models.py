from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128, unique=True) # Russian text.
    cover = models.ImageField(upload_to='small', blank=True)
    description = models.CharField(max_length=1000, default='Нет описания.')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128) # Russian.

    date = models.DateField(default=now().date())
    description = models.CharField(max_length=255, default='', blank=True)

    cover = models.ImageField(upload_to='small', blank=True)
    image = models.ImageField(upload_to='large', blank=True)
    multipage = models.BooleanField(default=False)
    link = models.URLField(blank=True)

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Page(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='large', blank=False)

    likes = models.IntegerField(default=0)

    def __str__(self):
        return 'Page of ' + self.product.name # + str(self.id)

class UserProfile(models.Model):
    # Link UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    score = models.IntegerField(default=0)
    bonus = models.IntegerField(default=10)

    #last_login = models.DateField(default=now().date())

    def __str__(self):
        return self.user.username
