from django.shortcuts import render, redirect
from product.models import Files_upload
from django.contrib.auth.decorators import login_required

# Create your views here.

cut_value = None

def cut(request, pk):
    pass

@login_required
def clear(request, pk):
    file = Files_upload.objects.get(pk=pk)
    if request.user == file.user:
        file.delete()
    return redirect('dashboard')

@login_required
def clear_all(request):
    files = Files_upload.objects.filter(user=request.user).all()
    if len(files) > 0:
        for file in files:
            file.delete()
    return redirect('dashboard')