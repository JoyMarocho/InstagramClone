from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='images/', default='default.png')
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

def save_profile(self):
        self.user

def delete_profile(self):
        self.delete()

@classmethod
def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

class Post(models.Model):
    image = models.ImageField(upload_to='posts/')
    name = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

@property
def get_all_comments(self):
        return self.comments.all()

def save_image(self):
        self.save()

def delete_image(self):
        self.delete()

def total_likes(self):
        return self.likes.count()

def __str__(self):
                return f'{self.user.name} Post'

class Comment(models.Model):
            comment = models.TextField()
            post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
            user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
            created = models.DateTimeField(auto_now_add=True, null=True)

            class Meta:
                ordering = ["-pk"]
        
            def __str__(self):
                return f'{self.user.name} Post'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Image', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user","post")

    def __str__(self):
        return 'Like: '+self.user.username+''+self.post.name


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'


