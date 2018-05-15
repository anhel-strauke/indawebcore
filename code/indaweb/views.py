from django.shortcuts import render

# Create your views here.

def index_stub(request):
    return render(request, "index_stub.html")
