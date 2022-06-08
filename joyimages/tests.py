from django.test import TestCase
from .models import Image, Profile

# Create your tests here.
class TestProfileClass(TestCase):
    def setUp(self):
        self.user = User(username='joy')
        self.user.save()
        
        self.new_profile = Profile(id=1, name = 'joy', profile_photo = 'image.jpg', bio = 'Dedicated coder',user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))

    def test_save_method(self):
        self.new_profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)


class TestImageClass(TestCase):
    def setUp(self):
        self.new_profile = Profile(name = 'the_joy', profile_photo = 'image.jpg', bio = 'Dedicated coder')
        self.new_profile.save_profile()

        self.new_image = Image(name = 'Coding Time', captions ='Coding is therapeutic', comments = 'What a cool image and message', photo = 'image.jpeg', likes = '2', profile = 'self.new_profile')
        self.new_image.save_image()

def tearDown(self):
    Profile.objects.all().delete()
    Image.objects.all().delete()
    
class TestPost(TestCase):
    def setUp(self):
        self.profile_test = Profile(name='joy', user=User(username='jojo'))
        self.profile_test.save()

        self.image_test = Post(image='image.png', name='test', caption='default test', user=self.profile_test)

    def test_insatance(self):
        self.assertTrue(isinstance(self.image_test, Post))

    def test_save_image(self):
        self.image_test.save_image()
        images = Post.objects.all()
        self.assertTrue(len(images) > 0)

    def test_delete_image(self):
        self.image_test.delete_image()
        after = Profile.objects.all()
        self.assertTrue(len(after) < 1)