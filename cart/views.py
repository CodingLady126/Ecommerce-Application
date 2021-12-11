from django.shortcuts import render,redirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages


from user.models import UserProfile
from shop.models import Product,Category
from .models import Cart,CartItem


@login_required
def check_out(request):
    #get the user
    user = request.user

    #Session update
    #set the user's num cart
    request.session["num_cart"] = str(0)

    try:
        #get the user cart or create if not one in the database
        cart = Cart.objects.get(user=user)
    except:
        #redirect if the item is already deleted
        return redirect(reverse('home'))
    if cart:
        cart.delete()
    
    #add success message to show to the user
    messages.info(request, 'Cart, checkout succesfully!!')
    return redirect(reverse('home'))

@login_required
def add_to_cart(request,product_id):
    #get the user
    user = request.user

    #get the user cart or create if not one in the database
    cart, new_created = Cart.objects.get_or_create(user=user)

    #get the product object from the db selected by the user
    selected_product = Product.objects.filter(id=product_id).first()
    cart_items = cart.cart_items
    cart_item = cart.cart_items.filter(product=selected_product).first()
    
    #check if alredy that item exist in the cart
    if cart_item: 
        #the item is in the cart
        #update the item in the cart and save
        cart_item.quantity += 1
        cart_item.save()
    else:
        #create new cart item for the product
        CartItem.objects.create(product = selected_product,cart = cart)       
    
    #Session update
    #set the user's num cart
    num_items = cart.getItems()
    request.session["num_cart"] = str(num_items)


    #add success message to show to the user
    messages.info(request, 'Item successfully added to the cart')

    #return back to the page
    next_url = request.GET['next'] if request.GET['next'] is not None else 'home'
    return redirect(next_url)


@login_required
def cart(request):
    #get the user
    user = request.user

    #get the user cart or create if not one in the database
    cart, new_created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cart_items
    
    #check if cart is empty
    if not cart_items :
        #cart is empty
        return render(request,'cart.html')

    #billing data
    data = {}
    total = 0

    for cart_item in cart_items.all():
        if cart_item.quantity > 0:
            price = int(cart_item.product.price*cart_item.quantity)
            data[cart_item.product] = [cart_item.quantity,price]
            total += price
    
    print(total)
    return render(request,'cart.html',context={
        'data':data,
        'total':total,
        'title':'cart'
    })

@login_required
def update_cart(request):
    #check if there is productd id and qty
    if(not request.GET['product_id'] or not request.GET['qty']):
        return redirect(reverse('home'))

    product_id = request.GET['product_id']
    product_qty = request.GET['qty']
    
    #get the user
    user = request.user

    #get the user cart or create if not one in the database
    cart, new_created = Cart.objects.get_or_create(user=user)

    #get the product object from the db selected by the user
    selected_product = Product.objects.get(id=product_id)
    cart_items = cart.cart_items
    cart_item = cart.cart_items.filter(product=selected_product).first()
    
    #check if alredy that item exist in the cart
    if cart_item: 
        #the item is in the cart
        #update the item in the cart and save

        #check if the qunatity is same
        if cart_item.quantity == int(product_qty):
            #no update needed
            #return back to the page
            return redirect(reverse('product_details', kwargs={'product_id':product_id}))

        cart_item.quantity = int(product_qty)
        cart_item.save()
    else:
        #create new cart item for the product
        CartItem.objects.create(product = selected_product,quantity=product_qty,cart = cart)       
    
    #Session update
    #set the user's num cart
    num_items = cart.getItems()
    request.session["num_cart"] = str(num_items)


    #add success message to show to the user
    messages.info(request, 'Cart successfully updated')

    #return back to the page
    return redirect(reverse('product_details', kwargs={'product_id':product_id}))