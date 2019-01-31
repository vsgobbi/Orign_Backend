from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

ACTUAL_YEAR = datetime.datetime.now()


class Vehicle(models.Model):

    key = models.AutoField(primary_key=True)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1950), MaxValueValidator(ACTUAL_YEAR.year)],
                                       help_text="""Fabrication year of <b>owner</b> car""")

    def __str__(self):
        return "Key: {} - year: {}".format(self.key, self.year)

    #def __unicode__(self):
    #    return self.year


class House(models.Model):

    stats = (
        ('owned', 'owned'),
        ('mortgaged', 'mortgaged'),
    )

    key = models.AutoField(primary_key=True)
    ownership_status = models.CharField(choices=stats, max_length=1,
                                        help_text="House ownership of <b>owner</b> house")
    def __str__(self):
        return "Key: {} - ownership_status: {}".format(self.key, self.ownership_status)


class Client(models.Model):

    marital_choices = (
        ('single', 'single'),
        ('married', 'married')
    )
    insurance_choices = (
        ('[0, 0, 1]', 'responsible'),
        ('[0, 1, 0]', 'regular'),
        ('[1, 0, 0]', 'economic')
    )

    age = models.PositiveIntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
    dependents = models.PositiveIntegerField(validators=[MinValueValidator(0)], null=False, blank=False,
                                             help_text="Number of <b>Client</b> family dependents")
    income = models.PositiveIntegerField(validators=[MinValueValidator(0)], null=False,
                                         help_text="Amount of income of <b>Client</b> in a year")
    marital_status = models.CharField(choices=marital_choices, max_length=1, null=False)
    vehicles = models.ManyToManyField(Vehicle, blank=True)
    houses = models.ManyToManyField(House, blank=True)
    risk_questions = models.CharField(choices=insurance_choices, max_length=1)


class RiskScore(models.Model):

    insurance =\
        (
        ('0', 'economic'),
        ('1', 'regular'),
        ('2', 'regular'),
        ('3', 'responsible')
        )
    key = models.AutoField(primary_key=True)

    score = models.PositiveIntegerField(default=None, null=True)
    risk_scores = models.CharField(choices=insurance, max_length=1, default=None, null=True)
    auto = models.CharField(choices=insurance, max_length=1, null=True)
    home = models.CharField(choices=insurance, max_length=20, null=True)
    life = models.CharField(choices=insurance, max_length=20, null=True)
    umbrella = models.CharField(choices=insurance, max_length=20, null=True)
    disability = models.CharField(max_length=20, null=True)

    client = models.OneToOneField(Client, related_name='client', on_delete=models.CASCADE)
    vehicles = models.OneToOneField(Vehicle, related_name='riskscore', on_delete=models.CASCADE, null=True)
    houses = models.OneToOneField(House, related_name='riskscore', on_delete=models.CASCADE, null=True)

