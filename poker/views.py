import random
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import PlayerProfile, PokerTable, PokerSeat

def PlayerProfile(request):
    profile = PlayerProfile.objects.get(user=request.user)
    return render(request, 'casino/table.html', {'profile': profile})

def poker_table_page(request, table_id):
    poker_table = get_object_or_404(PokerTable, id=table_id)
    occupied_seats = PokerTable.objects.filter(table=poker_table)

    context = {
        'table' : poker_table,
        'occupied_seats' : occupied_seats,
    }
    return render(request, 'poker/table.html',context)