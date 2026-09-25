import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import transaction
from .models import PlayerProfile, SlotMachine, SlotSpin, GameTransaction

@login_required
def play_slots(request, machine_id):
    machine = get_object_or_404(SlotMachine, id=machine_id, is_active=True)
    profile = get_object_or_404(PlayerProfile, user=request.user)

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
    return render(request, 'casino/slots.html', context)