from django.shortcuts import render, redirect
from .models import Portfolio, ContactRequest, Category
from django.contrib import messages
from users.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import WebsiteOrderForm, TelegramBotOrderForm

def web_design_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                phone = profile.phone
                name = request.user.username
                if not phone:
                    messages.error(request, "Please add a phone number to your profile")
                    return render(request, 'services/web_design.html', {'from_post': True, 'not_phone': True})
                ContactRequest.objects.create(name=name, phone=phone)
                messages.success(request, 'Your request has been submitted successfully!')
                return render(request, 'services/web_design.html', {'from_post': True})
            except Profile.DoesNotExist:
                messages.error(request, "Please complete your profile with a phone number")
                return redirect('update_user')
        else:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            if name and phone:
                # phone number validation
                if not phone.isdigit():
                    messages.error(request, "The phone number should only contain digits!")
                    return render(request, "services/web_design.html", {'from_post': True})
                elif len(phone) not in [11, 12]:
                    messages.error(request, "The phone number should be 11 or 12 digits long!")
                    return render(request, "services/web_design.html", {'from_post': True})
                elif not (phone.startswith('09') or phone.startswith('98')):
                    messages.error(request, 'The phone number should start with 09 or 98!')
                    return render(request, "services/web_design.html", {'from_post': True})
                else:
                    ContactRequest.objects.create(name=name, phone=phone)
                    messages.success(request, 'Your request has been submitted successfully')
                    return render(request, "services/web_design.html", {'from_post': True})
            else:
                messages.error(request, 'Please fill in all required fields.')
            return render(request, "services/web_design.html", {'from_post': True})
    messages.get_messages(request)
    return render(request, "services/web_design.html", {'from_post': False})


def web_design_portfolio_view(request):
    web_design_category = Category.objects.get(name="web design")
    portfolios = Portfolio.objects.filter(category=web_design_category)
    return render(request, "services/web_design_portfolio.html", {'portfolios': portfolios})



@login_required
def web_design_order_form_view(request):
    if request.method == 'POST':
        form = WebsiteOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, "Your order sent successfully and wait for the response")
            return render(request, "services/web_design_order_form.html", {'form': form, 'from_post': True})
        else:
            messages.error(request, 'Please check the form errors')
            return render(request, 'services/web_design_order_form.html', {'form': form, 'from_post': True})
    else:
        form = WebsiteOrderForm()
    messages.get_messages(request)
    return render(request, "services/web_design_order_form.html", {'form': form, 'from_post': False})
 

def telegram_bot_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                phone = profile.phone
                name = request.user.username
                if not phone:
                    messages.error(request, "Please add a phone number to your profile")
                    return render(request, 'services/telegram_bot.html', {'from_post': True})
                ContactRequest.objects.create(name=name, phone=phone)
                messages.success(request, 'Your request has been submitted successfully!')
                return render(request, 'services/telegram_bot.html', {'from_post': True})
            except Profile.DoesNotExist:
                messages.error(request, "Please complete your profile with a phone number")
                return redirect('update_user')
        else:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            if name and phone:
                # phone number validation
                if not phone.isdigit():
                    messages.error(request, "The phone number should only contain digits!")
                    return render(request, "services/telegram_bot.html", {'from_post':True})
                elif len(phone) not in [11, 12]:
                    messages.error(request, "The phone number should be 11 or 12 digits long!")
                    return render(request, "services/web_telegram_botdesign.html", {'from_post':True})
                elif not (phone.startswith('09') or phone.startswith('98')):
                    messages.error(request, 'The phone number should start with 09 or 98!')
                    return render(request, "services/telegram_bot.html", {'from_post':True})
                else:
                    ContactRequest.objects.create(name=name, phone=phone)
                    messages.success(request, 'Your request has been submitted successfully')
                    return render(request, "services/telegram_bot.html", {'from_post':True})
            else:
                messages.error(request, 'Please fill in all required fields.')
            return render(request, "services/telegram_bot.html", {'from_post':True})
    messages.get_messages(request)
    return render(request, "services/telegram_bot.html", {'from_post': False})


def telegram_bot_portfolio_view(request):
    telegram_bot_category = Category.objects.get(name="telegram bot")
    portfolios = Portfolio.objects.filter(category=telegram_bot_category)
    return render(request, "services/telegram_bot_portfolio.html", {'portfolios': portfolios})


@login_required
def telegram_bot_order_form_view(request):
    if request.method == "POST":
        form = TelegramBotOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, "Your order sent successfully and wait for the response")
            return render(request, "services/telegram_bot_order_form.html", {'form': form, 'from_post': True})
        else:
            messages.error(request, "Please check the form errors")
            return render(request, "services/telegram_bot_order_form.html", {'form': form, 'from_post': True})
    else:
        form = TelegramBotOrderForm()
    messages.get_messages(request)
    return render(request, "services/telegram_bot_order_form.html", {'form': form, 'from_post': False})
