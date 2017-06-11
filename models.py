from django.db import models
from enumfields import (
    EnumField,
    Enum
)

# Create your models here.


class Clearance(Enum):
    IR = 0
    R = 1
    O = 2
    Y = 3
    G = 4
    B = 5
    I = 6
    V = 7
    U = 8


class PlayerManager(models.Manager):
    """
        A default filter to avoid duplicate code and testing with not enabled users
    """
    def get_queryset(self):
        return super(PlayerManager, self).get_queryset().filter(enabled=True)


class Player(models.Model):
    telegram_id = models.IntegerField()
    name = models.CharField(max_length=40)
    gm = models.BooleanField(default=False)
    clearance = EnumField(Clearance, max_length=1)
    home_sector = models.CharField(max_length=3)
    clone_number = models.IntegerField(default=1)
    custom_player_name = models.CharField(max_length=50, blank=True)
    pp = models.IntegerField(default=25)
    credits = models.IntegerField(default=1000)
    # For debugging / testing purposes
    enabled = models.BooleanField(default=False)

    objects = PlayerManager()

    def get_player_name(self):
        if not self.custom_player_name or self.custom_player_name == "":
            return "{0.name}-{0.clearance}-{0.home_sector}-{0.clone_number}".format(self)
        return self.custom_player_name

    def set_custom_player_name(self, name):
        self.custom_player_name = name

    def increment_clearance(self):
        self.clearance = Clearance(self.clearance.value + 1)

    def decrement_clearance(self):
        self.clearance = Clearance(self.clearance.value - 1)

    def increment_clone(self):
        self.clone_number += 1

    def decrement_clone(self):
        self.clone_number -= 1

    def add_pp(self, number):
        self.pp += number

    def remove_pp(self, number):
        self.pp -= number

    def add_credits(self, number):
        self.credits += number

    def remove_credits(self, number):
        self.credits -= number

    def __str__(self):
        return self.get_player_name()


class Game(models.Model):
    channel_id = models.IntegerField(max_length=50)


class Snippet(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=1000)
    added_by = models.CharField(max_length=100, blank=True)
    added_via = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "{0.key} {0.value}".format(self)