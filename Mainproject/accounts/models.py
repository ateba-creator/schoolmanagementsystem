from django.contrib.auth.models import AbstractUser, BaseUserManager,User
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#from administration.models import Classroom

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_no, password=None, **extra_fields):
        """Create and save a User with the given phone_no and password."""
        if not phone_no:
            raise ValueError('The given phone_no must be set')
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('User must have is_staff=True.')
        return self._create_user(phone_no, password, **extra_fields)



    def create_superuser(self, phone_no, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('nationality', '')
        extra_fields.setdefault('place_of_birth', '')
        extra_fields.setdefault('religion', '')
        extra_fields.setdefault('gender', '')
        extra_fields.setdefault('marital_status', '')
        extra_fields.setdefault('address', '')


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_no, password, **extra_fields)

class Teacher(AbstractUser):
    nationality_choice = (
        ('Afrique du Sud','Afrique du Sud'),
        ('Algérie','Algérie'),
        ('Angola','Angola'),
        ('Bénin','Bénin'),
        ('Botswana','Botswana'),
        ('Burkina Faso','Burkina Faso'),
        ('Burundi','Burundi'),
        ('Cameroun','Cameroun'),
        ('Cap-Vert','Cap-Vert'),
        ('République centrafricaine','République centrafricaine'),
        ('Comores','Comores'),
        ('République du Congo','République du Congo'),
        ('République démocratique du Congo','République démocratique du Congo'),
        ('Côte d’Ivoire','Côte d’Ivoire'),
        ('Djibouti','Djibouti'),
        ('Égypte','Égypte'),
        ('Érythrée','Érythrée'),
        ('Eswatini','Eswatini'),
        ('Éthiopie','Éthiopie'),
        ('Gabon','Gabon'),
        ('Gambie','Gambie'),
        ('Ghana','Ghana'),
        ('Guinée','Guinée'),
        ('Guinée-Bissau','Guinée-Bissau'),
        ('Guinée équatoriale','Guinée équatoriale'),
        ('Kenya','Kenya'),
        ('Lesotho','Lesotho'),
        ('Liberia','Liberia'),
        ('Libye','Libye'),
        ('Madagascar','Madagascar'),
        ('Malawi','Malawi'),
        ('Mali','Mali'),
        ('Maroc','Maroc'),
        ('Maurice','Maurice'),
        ('Mauritanie','Mauritanie'),
        ('Mozambique','Mozambique'),
        ('Naminie','Namibie'),
        ('Niger','Niger'),
        ('Nigeria','Nigeria'),
        ('Ouganda','Ouganda'),
        ('Rwanda','Rwanda'),
        ('São Tomé-et-Principe','São Tomé-et-Principe'),
        ('Sénégal','Sénégal'),
        ('Seychelles','Seychelles'),
        ('Sierra Leone','Sierra Leone'),
        ('Somalie','Somalie'),
        ('Soudan','Soudan'),
        ('Soudan du Sud','Soudan du Sud'),
        ('Tanzanie','Tanzanie'),
        ('Tchad','Tchad'),
        ('Togo','Togo'),
        ('Tunisie','Tunisie'),
        ('Zambie','Zambie'),
        ('Zimbabwe','Zimbabwe'),
    )
    SEX = (
        ('masculin', 'masculin'),
        ('feminin', 'feminin')
    )
    marital_status_choice = (
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('divorced', 'Divorced'),
        ('single', 'Single')
    )
    religion_choice = (
        ('christianisme','christianisme'),
        ('islam','islam')
    )
    #General fields
    username = None
    user = models.OneToOneField("Teacher", on_delete=models.CASCADE,null=True)
    photo = models.ImageField(null=True,blank=True,upload_to='profile_pictures/')
    date_of_birth = models.CharField(max_length=20)
    place_of_birth = models.CharField(max_length=45)
    nationality = models.CharField(max_length=45, choices=nationality_choice,default='Cameroun')
    religion = models.CharField(max_length=45, choices=religion_choice,default='christianisme')
    gender = models.CharField(choices=SEX, max_length=10)
    phone_no = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=100)
    is_authorized = models.BooleanField(default=False, null=True)
    is_delete = models.BooleanField(default=False, null=True)
    classrooms = models.ManyToManyField('administration.Classroom', blank=True)

    #Teacher fields
    marital_status = models.CharField(choices=marital_status_choice, max_length=10)
    department = models.ManyToManyField("administration.Department",blank=True)

    sequence = models.ManyToManyField('academic.TeacherSequence')

    USERNAME_FIELD = 'phone_no'
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name
    @property
    def get_id(self):
        return self.user.id



