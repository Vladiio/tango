from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.views < 0:
            self.views *= -1
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    first_visit = models.DateTimeField(blank=True, null=True)
    last_visit = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        now = timezone.now()

        if self.first_visit > now:
            self.first_visit = now

        if self.last_visit > now:
            self.last_visit = now

        if self.last_visit < self.first_visit:
            self.last_visit = self.first_visit

        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
