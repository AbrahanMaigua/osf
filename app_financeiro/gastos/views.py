from django.shortcuts import render

# Create your views here.
def historial(request):
    return render(request, 'history.html')
def gastos(request):
    return render(request, 'gastos.html')
def metas(request):
    return render(request, 'metas.html')
