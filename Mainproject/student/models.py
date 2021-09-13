from django.db import models

class Student(models.Model):
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
    status = (
        ('Nouveau', 'Nouveau'),
        ('Ancien', 'Ancien')
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True, upload_to='profile_pictures/')
    date_of_birth = models.CharField(max_length=20)
    place_of_birth = models.CharField(max_length=45)
    nationality = models.CharField(max_length=45, choices=nationality_choice, default='Cameroun')
    religion = models.CharField(max_length=45, choices=religion_choice, default='christianisme')
    gender = models.CharField(choices=SEX, max_length=10)
    phone_no = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    fee = models.ManyToManyField('administration.Fee')
    is_delete = models.BooleanField(default=False, null=True)
    report_card = models.ManyToManyField('academic.Report_card',blank=True)
    year = models.ManyToManyField('academic.Date',blank=True)
    status = models.CharField(blank=True, null=True, max_length=10, choices=status, default='Nouveau')
    #Student fields
    parent = models.ForeignKey('accounts.Teacher', null=True, blank=True, on_delete=models.CASCADE)
    mother_name = models.CharField(max_length=100, null=True)
    father_name = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    locality = models.CharField(max_length=100, null=True)
    school_of_origin = models.CharField(max_length=100, null=True)
    course = models.ManyToManyField('administration.Course')
    matricule = models.CharField(null=True, blank=True, max_length=100)
    remark = models.ManyToManyField('academic.Remark', blank=True)
    absent_hours = models.ManyToManyField('academic.AbsentHours', blank=True)

    cards = models.ManyToManyField('academic.Card')
    honor_rolls = models.ManyToManyField('academic.HonorRoll')

    def __str__(self):
        return self.first_name
