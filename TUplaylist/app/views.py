from django.shortcuts import render

# Create your views here.
def debug_page(request):
    return render(request, "debug_page.html")