from django.shortcuts import render, get_object_or_404, redirect
from models.models import Subscription
from .forms import SubscriptionForm

def subscription_list(request):
    """Read: List all subscriptions"""
    subscriptions = Subscription.objects.all()
    return render(request, 'admin/subscriptions/subscription_list.html', {'subscriptions': subscriptions})

def subscription_create(request):
    """Create a new subscription"""
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()
    return render(request, 'admin/subscriptions/subscription_form.html', {'form': form, 'title': 'Add Subscription'})

def subscription_update(request, pk):
    """Update an existing subscription"""
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'admin/subscriptions/subscription_form.html', {'form': form, 'title': 'Edit Subscription'})

def subscription_delete(request, pk):
    """Delete a subscription"""
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == "POST":
        subscription.delete()
        return redirect('subscription_list')
    return render(request, 'admin/subscriptions/subscription_confirm_delete.html', {'subscription': subscription})
