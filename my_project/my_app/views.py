from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ItemForm
from .models import Item

# Register
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)

        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})

# Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# READ
@login_required
def item_list(request):
    items = Item.objects.filter(user=request.user)
    return render(request, 'item_list.html', {'items': items})

# CREATE
@login_required
def item_create(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()

        return redirect('item_list')
    return render(request, 'item_form.html', {'form': form})

# UPDATE
@login_required
def item_update(request, pk):
    item = Item.objects.get(pk=pk, user=request.user)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()

        return redirect('item_list')
    return render(request, 'item_form.html', {'form': form})

# DELETE
@login_required
def item_delete(request, pk):
    item = Item.objects.get(pk=pk, user=request.user)
    item.delete()
    
    return redirect('item_list')