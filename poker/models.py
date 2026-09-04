from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class playerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, releated_name="profile")

    balance = models.DecimalFiled(max_digits=12, decimal_places=2, default=1000.00)
    avatar = models.ImageFiled(upload_with='/avatars', blank=True, null=True)
    created_at = models.DataTimeFiled(auto_now_add=True)

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
    table = models.ForeingKey(PokerTable, on_delete=models.CASCADE, releated_name='seats')
    player = models.ForeingKey(playerProfile, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    chips_in_game = models.DecimalField(max_digits=10, decimal_places=2)
    player_cards = models.CharField(max_length=10, blank=True, default="")
    is_folded = models.BooleanField(default=False)

    class Meta:
        unique_together = ('table', 'seat-number')