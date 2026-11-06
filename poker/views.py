import random
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render , redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import transaction
from .models import PlayerProfile, SlotMachine, SlotSpin, GameTransaction
from django.shortcuts import render
def home(request):
    return render(request, 'casino/home.html')
from .models import PokerTable, SlotMachine


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')


def home(request):
    poker_tables = PokerTable.objects.all()
    slot_machines = SlotMachine.objects.filter(is_active=True)

    context = {
        "poker_tables": poker_tables,
        "slot_machines": slot_machines,
    }

    return render(request, "home.html", context)

@login_required
def play_slots(request, machine_id):
    machine = get_object_or_404(SlotMachine, id=machine_id, is_active=True)

    profile, created = PlayerProfile.objects.get_or_create(
    user=request.user,
    defaults={'balance': 1000}
)
    if request.method == 'POST':
        try:
            bet = Decimal(request.POST.get('bet_amount', 0))
        except ValueError:
            messages.error(request, "Некорректная сумма ставки.")
            return redirect('slots_page', machine_id=machine.id)

        if bet < machine.min_bet or bet > machine.max_bet:
            messages.error(request, f"Ставка должна быть в пределах от {machine.min_bet} до {machine.max_bet}")
            return redirect('slots_page', machine_id=machine.id)

        if profile.balance < bet:
            messages.error(request, "Недостаточно средств для ставки!")
            return redirect('slots_page', machine_id=machine.id)


        symbols = ['🍒', '🍋', '🔔', '7️⃣']
        reel1 = random.choice(symbols)
        reel2 = random.choice(symbols)
        reel3 = random.choice(symbols)
        combination_str = f"{reel1} | {reel2} | {reel3}"

      
        win_amount = Decimal('0.00')
        if reel1 == reel2 == reel3:
            if reel1 == '7️⃣':
                win_amount = bet * 10  
            else:
                win_amount = bet * 3  
        elif reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
            win_amount = bet * Decimal('1.5') 


          
            balance_change = win_amount - bet
            profile.balance += balance_change
            profile.save()

  
            SlotSpin.objects.create(
                player=profile,
                machine=machine,
                bet_amount=bet,
                win_amount=win_amount,
                combination=combination_str
            )

    
            if balance_change != 0:
                GameTransaction.objects.create(
                    player=profile,
                    amount=balance_change,
                    game_type='SLOTS',
                    description=f"Крутка на автомате {machine.name}. Результат: {combination_str}"
                )

        if win_amount > 0:
            messages.success(request, f"Победа! Выпало [{combination_str}]. Вы выиграли {win_amount}!")
        else:
            messages.error(request, f"Увы! Выпало [{combination_str}]. Ставка {bet} потеряна.")


    last_spin = SlotSpin.objects.filter(player=profile, machine=machine).last()

    context = {
        'machine': machine,
        'profile': profile,
        'last_spin': last_spin
    }

def durak(request):
    return render(request, 'durak.html')

    return render(request, 'slots.html', context)
    return redirect('slots_page', machine_i=machine.id)