from django.shortcuts import render, HttpResponse
from django.views.generic import View, TemplateView

# def index_page(request):
#     return render(request, 'indexpage/index.html')

class IndexPageView(TemplateView):
    template_name = 'indexpage/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'key':'value'}) 
        return context
    