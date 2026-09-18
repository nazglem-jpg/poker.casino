from django.contrib import admin
from .models import (
    GameTransaction,
    SlotMachine ,
    SlotSpin,
    PlayerProfile,
    PokerTable,
    PokerSeat,
)

admin.site.register(PlayerProfile)
admin.site.register(GameTransaction)
admin.site.register(SlotMachine)
admin.site.register(SlotSpin)
admin.site.register(PokerSeat)
admin.site.register(PokerTable)
# Register your models here.
