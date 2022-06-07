from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=35)
    caption = models.TextField(default='caption')
    photo = CloudinaryField('image',default='photo.jpeg')
    username = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    posted_on = models.DateTimeField(default=timezone.now)


class Meta:
    ordering = ['posted_on']

    def __str__(self):
        return self.name

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def get_absolute_url(self):
        return reverse('image-detail')

    # def update_image(self):
    #   fetched_object = Image.objects.filter(author=current_value).update(author=new_value)
    #   return fetched_object


class Profile(models.Model):
    name = models.CharField(max_length=70, default='Phi')
    profile_photo = CloudinaryField('image', default='img.jpg')
    bio = models.TextField(default='Add Bio here')

    def __str__(self):
        return self.name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Image', null=True, on_delete=models.CASCADE, related_name='comment')
    body = models.TextField(default='Comment Here')
    posted_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)

class Meta:
    ordering = ['posted_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Image', on_delete=models.CASCADE)

class Meta:
    unique_together = ("user","post")

    def __str__(self):
        return 'Like: '+self.user.username+''+self.post.name


class Followers(models.Model):
    user = models.CharField(max_length=50, default='')
    follower = models.CharField(max_length=50, default='')


