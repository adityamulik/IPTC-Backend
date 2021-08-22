from django.shortcuts import render
from django.http import HttpResponse

def api_home(request):
    """
    returns api home page.
    """
    return HttpResponse("<h1>IPTC API Homepage</h1>")
