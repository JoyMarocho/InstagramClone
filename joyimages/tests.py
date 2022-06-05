from django.test import TestCase
from .models import Image, Profile

# Create your tests here.
class TestProfileClass(TestCase):
    def setUp(self):
        self.new_profile = Profile(name = 'the_joy', profile_photo = 'image.jpg', bio = 'Dedicated coder')

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