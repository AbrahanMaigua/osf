from django.shortcuts import render

# Create your views here.
def profile(request):
    return render(request, 'profile.html')
def login(request):
    return render(request, 'login.html')
def sigin(request):
    return render(request, 'sigin.html')
