from datetime import datetime
from email.policy import default
from msilib.schema import Class
from pyexpat import model

from django.db import models

# Create your models here.

class Settlement(models.Model):
    class level (models.IntegerChoices):
        Hamlet = 1
        Village = 2
        Tiny_Town = 3
        Big_town = 4
        City = 5
        Major_City = 6
        Metropolis = 7 
    settlement_name = models.CharField(max_length=200)
    settlement_level = models.IntegerField(choices=level.choices)
    settlement_location = models.CharField(max_length=200)
    population = models.IntegerField(default=0)
    def __str__(self):
        return self.settlement_name

class Character(models.Model): 
    character_name = models.CharField(max_length=200)
    character_function = models.CharField(max_length=200)
    character_first_contact = models.CharField(max_length=200)
    character_information = models.TextField(max_length=450)
    character_added_information = models.TextField(max_length=450)
    def __str__(self):
        return self.character_name

class Building(models.Model):
    class type(models.IntegerChoices):
        Management = 1
        Commercial = 2
        Military_Or_Adventuring = 3
        Educational = 4
    building_title = models.CharField(max_length=200)
    building_description = models.TextField(max_length=450)
    type = models.IntegerField(choices=type.choices)
    level = models.IntegerField(default=0)
    cost = models.IntegerField()
    pop_mod = models.DecimalField(max_digits=5, decimal_places=2)
    tenant = models.ForeignKey(Character, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return (self.building_title)

class Event(models.Model): 
    event_name = models.CharField(max_length=200)
    event_desc = models.TextField(max_length=450)
    event_effect = models.TextField(max_length=450)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.event_name

class ShopItem(models.Model):
    models.ForeignKey(Building, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    item_descr = models.CharField(max_length=200)
    item_URL = models.URLField(max_length=200)
    item_cost = models.IntegerField(default=50)
    item_stock = models.IntegerField(default=1)
    item_active = models.BooleanField(default=True)
    def __str__(self):
        return self.item_name

class Funds(models.Model):
    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE)
    pos_change = models.IntegerField(default=0)
    neg_change = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    class Meta:
        verbose_name_plural = "funds"

    def __str__(self):
        return f'+{self.pos_change} , -{self.neg_change}'

