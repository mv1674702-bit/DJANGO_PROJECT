from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ItemForm
from .models import Item
from django.contrib.auth.models import User

# Register
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')
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