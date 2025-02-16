from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dash:home')
    if request.method == 'POST':
        try: 
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(password)
            # Example validation checks (replace with actual logic)
            errors = []
            if not username:
                errors.append(_("Username is required."))
            if not password:
                errors.append(_("Password is required."))

            if errors:
                # If errors, return them as a JSON response
                return JsonResponse({'errors': errors})
            
            # Authentication and login logic (you can replace with actual user login)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return JsonResponse({'redirect_url': reverse('dash:home')})  # Redirect to dashboard or another page
            else:
                return JsonResponse({'errors': [_('Invalid credentials.')]})
        except Exception as e:
            print(e)

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('frontend:home')  # Redirects to the homepage (or any page you choose)