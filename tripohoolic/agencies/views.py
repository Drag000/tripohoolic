from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index_agencies(request):
    return render(request,'agencies/agencies.html')
