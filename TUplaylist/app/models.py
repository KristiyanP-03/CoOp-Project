from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date




from django.contrib.auth.models import Group, Permission



# Create your models here.


# Profile Model
# #=====================================================================================================================
def username_length(value):
    if len(value) < 2:
        raise ValidationError("Username must be at least 2 characters long.")
def no_spaces(input):
    if " " in input:
        raise ValidationError("You can't use white spaces")

class ProfileModel(AbstractUser):
    username = models.CharField(verbose_name="Username", unique=True, validators=[no_spaces, username_length])
    email = models.EmailField(verbose_name="Email", unique=True)
    profile_picture = models.URLField(verbose_name="Profile Picture (URL)", blank=True, null=True)
    bio = models.TextField(verbose_name="Bio", blank=True, null=True)



# Song Model
#=======================================================================================================================
current_year = date.today().year


class SongModel(models.Model):
    ARTIST_TYPE_CHOICES = (
        ('artist', 'Artist'),
        ('band', 'Band'),
    )

    GENRE_CHOICES = (
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('hiphop', 'Hip-Hop'),
        ('aesthetic_rap', 'Aesthetic Rap'),
        ('jazz', 'Jazz'),
        ('classical', 'Classical'),
        ('electronic', 'Electronic'),
        ('house', 'House'),
        ('hardstyle', 'Hardstyle'),
        ('techno', 'Techno'),
        ('folk', 'Folk'),
        ('indie', 'Indie'),
        ('metal', 'Metal'),
        ('punk', 'Punk'),
        ('rnb', 'R&B'),
        ('country', 'Country'),
        ('reggae', 'Reggae'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=100, verbose_name="Title")
    artist = models.CharField(max_length=100, verbose_name="Artist / Band Name")
    artist_type = models.CharField(max_length=10, choices=ARTIST_TYPE_CHOICES, verbose_name="Type (Artist or Band)")
    release_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1888),
            MaxValueValidator(current_year)
        ],
        verbose_name="Release Year"
    )
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, verbose_name="Genre")
    cover = models.URLField(verbose_name="Cover Image URL", blank=True, null=True)
    duration = models.DurationField(verbose_name="Duration")
    uploader = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Uploaded By")
