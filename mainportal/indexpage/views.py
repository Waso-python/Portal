from django.shortcuts import render, HttpResponse

def index_page(request):
    return render(request, 'indexpage/index.html')
