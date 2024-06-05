from django.shortcuts import render

# Create your views here.
def categorias(request):
   return render(request, 'categorias.html', context={'title':'Categorias'})

def detail(request, categoria_id:int):
   return render(request, 'detail.html', context={'title':'Categorias'})

def subcategoria(request, categoria_id:int):
   return render(request, 'detail.html', context={'title':'Categorias'})