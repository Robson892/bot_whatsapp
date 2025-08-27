from django.shortcuts import render, get_object_or_404, redirect
from .models import WhatsAppBot, Trigger, Conversation
from .forms import WhatsAppBotForm, TriggerForm

def dashboard(request):
    bots = WhatsAppBot.objects.all()
    conversations = Conversation.objects.all().order_by('-created_at')[:10]
    return render(request, 'whatsapp/dashboard.html', {'bots': bots, 'conversations': conversations})

def bot_list(request):
    bots = WhatsAppBot.objects.all()
    return render(request, 'whatsapp/bot_list.html', {'bots': bots})

def bot_create(request):
    if request.method == 'POST':
        form = WhatsAppBotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bot_list')  # redireciona para a lista de bots
    else:
        form = WhatsAppBotForm()
    return render(request, 'whatsapp/bot_create.html', {'form': form})


def bot_detail(request, pk):
    bot = get_object_or_404(WhatsAppBot, pk=pk)
    triggers = Trigger.objects.filter(bot=bot)

    if request.method == 'POST':
        form = TriggerForm(request.POST)
        if form.is_valid():
            new_trigger = form.save(commit=False)
            new_trigger.bot = bot  # associa o trigger ao bot
            new_trigger.save()
            return redirect('bot_detail', pk=bot.pk)
    else:
        form = TriggerForm()

    return render(request, 'whatsapp/bot_detail.html', {
        'bot': bot,
        'triggers': triggers,
        'form': form,
    })
