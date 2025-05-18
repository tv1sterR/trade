from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import ExchangeOffer, Product

def home(request):
    posts = Product.objects.filter(is_active=True)
    for post in posts:
        post.condition_display = "Новый" if post.condition == 'new' else 'БУ'
    return render(request, 'app/index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        post = Product.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            photo=request.POST.get("image_url", ""),
            category=request.POST.get("category"),
            condition=request.POST.get("condition")
        )
        return render(request, "app/post_created.html", {"post": post})
    return render(request, 'app/create_post.html')

def post_details(request, post_id):
    post = get_object_or_404(Product, id=post_id)
    return render(request, 'app/post_details.html', {'post': post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Product, id=post_id, user=request.user)

    if request.method == "POST":
        post.title = request.POST['title']
        post.description = request.POST['description']
        post.photo = request.POST['photo']
        post.category = request.POST['category']
        post.condition = request.POST['condition']
        post.save()
        return redirect('post_details', post_id=post.id)
    return render(request, 'app/edit_post.html', {'post': post})

@login_required()
def delete_post(request, post_id):
    post = get_object_or_404(Product, id=post_id, user=request.user)
    post.delete()
    return redirect('home')

def search_post(request):
    query = request.GET.get('q', '')
    categories = Product.objects.values_list("category", flat=True).distinct()

    posts = Product.objects.filter(Q(title__icontains=query) |
                                    Q(description__icontains=query) |
                                    Q(category__icontains=query)
    ).order_by("-created_at") if query else []

    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/search_post.html', {'posts': page_obj, 'query': query, 'categories': categories})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('home')

def exchange_post(request, post_id):
     post_receiver = get_object_or_404(Product, id=post_id)

     if request.method == "POST":
         post_sender_id = request.POST.get("post_sender_id")
         comment = request.POST.get("comment")

         post_sender = get_object_or_404(Product, id=post_sender_id, user=request.user)

         offer = ExchangeOffer.objects.create(
             sender=request.user,
             post_sender=post_sender,
             post_receiver=post_receiver,
             comment=comment
         )
         return redirect("exchange_list")

     user_posts = Product.objects.filter(user=request.user)
     return render(request, 'app/exchange.html', {'post_receiver': post_receiver, 'user_posts': user_posts})

@login_required
def exchange_list(request):
    offers = ExchangeOffer.objects.filter(sender=request.user) | ExchangeOffer.objects.filter(post_receiver__user=request.user)
    status_filter = request.GET.get("status")
    if status_filter:
        offers = offers.filter(status=status_filter)

    return render(request, 'app/exchange_list.html', {'offers': offers})

@login_required
def update_exchange(request, offer_id):
    offer = get_object_or_404(ExchangeOffer, id=offer_id, post_receiver__user=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ['accepted', 'declined']:
            offer.status = new_status
            offer.save()
            if new_status == "accepted":
                offer.post_sender.is_active = False
                offer.post_sender.save()
                offer.post_receiver.is_active = False
                offer.post_receiver.save()
        return redirect("exchange_list")
    return render(request, 'app/update_exchange.html', {'offer': offer})

@login_required
def cancel_exchange(request, offer_id):
    offer = get_object_or_404(ExchangeOffer, id=offer_id)

    if request.user == offer.sender:
        offer.delete()
        return redirect("exchange_list")
    return redirect("exchange_list")
