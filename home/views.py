from django.shortcuts import render, redirect
from services.models import ContactRequest
from django.contrib import messages
from users.models import Profile

def home(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                phone = profile.phone
                name = request.user.username
                if not phone:
                    messages.error(request, "Please add a phone number to your profile")
                    return render(request, 'home/index.html', {'from_post': True, 'not_phone': True})
                ContactRequest.objects.create(name=name, phone=phone, source=source)
                messages.success(request, 'Your request has been submitted successfully!')
                return render(request, 'home/index.html', {'from_post': True})
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
                    return render(request, 'home/index.html', {'from_post': True})
                elif len(phone) not in [11, 12]:
                    messages.error(request, "The phone number should be 11 or 12 digits long!")
                    return render(request, 'home/index.html', {'from_post': True})
                elif not (phone.startswith('09') or phone.startswith('98')):
                    messages.error(request, 'The phone number should start with 09 or 98!')
                    return render(request, 'home/index.html', {'from_post': True})
                else:
                    ContactRequest.objects.create(name=name, phone=phone, source=source)
                    messages.success(request, 'Your request has been submitted successfully')
                    return render(request, 'home/index.html', {'from_post': True})
            else:
                messages.error(request, 'Please fill in all required fields.')
            return render(request, 'home/index.html', {'from_post': True})
    messages.get_messages(request)
    return render(request, 'home/index.html', {'from_post': False})


def about(request):
    return render(request, 'home/about.html', {})

def support(request):
    return render(request, 'home/support.html', {})

def contact(request):
    return render(request, 'home/contact.html', {})