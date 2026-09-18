from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=1000.00)
    avatar = models.ImageField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | Баланс: {self.balance}"

class PokerTable(models.Model):
    name = models.CharField(max_length=50, unique=True)
    small_blind = models.DecimalField(max_digits=6, decimal_places=2)
    big_blind = models.DecimalField(max_digits=6, decimal_places=2)
    max_seats = models.IntegerField(default=6)
    community_cards = models.CharField(max_length=20, blank=True, db_default="")
    pot = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_game_running = models.BooleanField(default=False)

    def __sts__(self):
        return f"Покер: {self.name} ({self.small_blind}/{self.big_blind})"

class PokerSeat(models.Model):
    table = models.ForeignKey(PokerTable, on_delete=models.CASCADE, related_name='seats')
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.PositiveIntegerField()
    chips_in_game = models.DecimalField(max_digits=10, decimal_places=2)
    player_cards = models.CharField(max_length=10, blank=True, default="")
    is_folded = models.BooleanField(default=False)

    class Meta:
        unique_together = ('table', 'seat_number')


class GameTransaction(models.Model):
    GAME_CHOICES = [
        ('POKER', 'Покер'),
        ('SLOTS', 'Слоти'),
        ('SYSTEM', 'Каса(Поповнення/Виведення )'),
    ]
    player = models.ForeignKey(PlayerProfile,on_delete=models.CASCADE,related_name='transactions' )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    game_type = models.CharField(max_length=10,choices=GAME_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class SlotMachine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_bet = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    max_bet = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    rtp = models.FloatField(default=96.5)
    is_active = models.BooleanField(default=True)
    def str(self):
        return f"Слот:{self.name}"

class SlotSpin(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='slot_spin')
    machine = models.ForeignKey(SlotMachine, on_delete=models.PROTECT, related_name = 'slot_spin')
    bet_amount = models.DecimalField(max_digits=8, decimal_places=2)
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    combination = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)