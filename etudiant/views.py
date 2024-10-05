from django.shortcuts import render

def index_view(request):
    ctx = {}
    return render(request, "index.html", ctx)