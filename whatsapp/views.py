from django.shortcuts import render, get_object_or_404, redirect
from .models import WhatsAppBot, Trigger, Conversation, User
from .forms import WhatsAppBotForm, TriggerForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import SignUpForm
from django.conf import settings
import stripe



# =======================
# HOME
# =======================

def home(request):
    return render(request, 'whatsapp/home.html')


# =======================
# DASHBOARD
# =======================
@login_required
def dashboard(request):
    bots = WhatsAppBot.objects.filter(owner=request.user)
    conversations = Conversation.objects.filter(bot__owner=request.user).order_by('-created_at')[:10]
    return render(request, "whatsapp/dashboard.html", {
        "bots": bots,
        "conversations": conversations,
    })
# =======================
# BOTS
# =======================
@login_required
def bot_list(request):
    bots = WhatsAppBot.objects.filter(owner=request.user)
    return render(request, 'whatsapp/bot_list.html', {'bots': bots})

@login_required
def bot_create(request):
    if request.method == 'POST':
        form = WhatsAppBotForm(request.POST)
        if form.is_valid():
            bot = form.save(commit=False)
            bot.owner = request.user  # associa o bot ao usuário logado
            bot.save()
            return redirect('bot_list')
    else:
        form = WhatsAppBotForm()
    return render(request, 'whatsapp/bot_create.html', {'form': form})

@login_required
def bot_detail(request, pk):
    bot = get_object_or_404(WhatsAppBot, pk=pk, owner=request.user)  # garante que o bot pertence ao user
    triggers = Trigger.objects.filter(bot=bot)

    if request.method == 'POST':
        form = TriggerForm(request.POST)
        if form.is_valid():
            new_trigger = form.save(commit=False)
            new_trigger.bot = bot
            new_trigger.save()
            return redirect('bot_detail', pk=bot.pk)
    else:
        form = TriggerForm()

    return render(request, 'whatsapp/bot_detail.html', {
        'bot': bot,
        'triggers': triggers,
        'form': form,
    })

@login_required
def bot_update(request, pk):
    # Busca apenas o bot do usuário logado
    bot = get_object_or_404(WhatsAppBot, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = WhatsAppBotForm(request.POST, instance=bot)
        if form.is_valid():
            form.save()
            messages.success(request, "Bot atualizado com sucesso!")
            return redirect('bot_list')
        else:
            messages.error(request, "Erro ao atualizar o bot. Verifique os dados.")
    else:
        form = WhatsAppBotForm(instance=bot)

    return render(request, 'whatsapp/bot_update.html', {'form': form, 'bot': bot})

# =======================
# LOGIN / LOGOUT
# =======================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "whatsapp/login.html")

@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

# =======================
# CADASTRO DE USUÁRIO
# =======================
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loga automaticamente
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'whatsapp/signup.html', {'form': form})





# =======================
# CHECKOUT
# ======================= 

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, 'whatsapp/home.html')

def checkout(request):
    plan = request.GET.get('plan')
    if plan == 'basico':
        price_id = settings.STRIPE_PRICE_ID_BASICO
    elif plan == 'profissional':
        price_id = settings.STRIPE_PRICE_ID_PROFISSIONAL
    else:
        return redirect('home')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return redirect(session.url)

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')
