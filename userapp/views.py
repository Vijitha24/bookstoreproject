import stripe
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from django.urls import reverse

from bookproj2app.models import Book,Author
from userapp.models import Cart, Cartitems


# Create your views here.

def user_listbook(request):
    books=Book.objects.all()
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=Paginator.page(page_number.num_pages)


    return render(request,'User/userbooklist.html',{'books':books,'page':page})

def user_detailsview(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request, 'User/userdetailview.html', {'book': book})

def usersearch_book(request):
    query=None
    books=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains= query) )
    else:
        books=[]
    context={'books':books,'query':query}
    return render(request, 'User/usersearch.html',context)

def add_to_cart (request,book_id):
    book=Book.objects.get(id=book_id)

    if book.quantity>0:
        cart,created=Cart.objects.get_or_create(user=request.user)
        cart_item,item_created=Cartitems.objects.get_or_create(cart=cart,book=book)

        if not item_created:
            cart_item.quantity+=1
            cart_item.save()
    return redirect('viewcart')
def view_cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_items=cart.cartitems_set.all()
    cart_item=Cartitems.objects.all()
    total_price=sum(item.book.price * item.quantity for item in cart_items)
    total_items=cart_items.count()

    context={'cart_items':cart_items,'cart_item':cart_item,'total_price':total_price,'total_items':total_items}
    return render(request,'User/cart.html',context)


def increase_quantity(request,item_id):
    cart_item=Cartitems.objects.get(id=item_id)
    if cart_item.quantity<cart_item.book.quantity:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('viewcart')

def decrease_quantity(request,item_id):
    cart_item = Cartitems.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('viewcart')

def remove_cart(request,item_id):
    try:
        cart_item = Cartitems.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass
    return redirect('viewcart')


def create_checkout_session(request):
    cart_items= Cartitems.objects.all()

    if cart_items:

        stripe.api_key=settings.STRIPE_SECRET_KEY

        if request.method=='POST':
            line_items=[]
            for cart_item in cart_items :
                if cart_item.book:
                    line_item={
                        'price_data' :{
                            'currency':'INR',
                            'unit_amount':int(cart_item.book.price * 100),
                            'product_data':{

                                'name': cart_item.book.title
                            },

                        },
                    'quantity':1
                    }
                    line_items.append(line_item)
            if line_items:
                checkout_session=stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel')),


                )
                return redirect(checkout_session.url,code=303)


def success(request):
    cart_items=Cartitems.objects.all()
    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()
    cart_items.delete()
    return render(request,'user/success.html')


def cancel(request):
    return render(request, 'user/cancel.html')




