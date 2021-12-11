from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse

from  shop.models import  Product,Category
# Create your views here.
def home_page(request):
    #get the latest 4 items added in the database
    latest = Product.objects.order_by('-date')[:4]
    categories = Category.objects.all()
    
    #gett 4 items from each categories
    categories_data = {}
    for category in categories:
        category_items = category.items.all()[:4]
        categories_data[category.name] = category_items

    #info to pass into the html template
    context = {
        'products_latest': latest,
        'products_cats':categories_data,
        'title':'home'
    }
    return render(request,'home.html',context)

def product_detail(request, product_id):
    #get the prodcut and render the html template
    try:
        product = Product.objects.get(id=product_id)
    except:
        #handing other urls that are not in the database
        return(redirect(reverse('home')))
    
    #quatiity of item in the user cart
    product_qunatity = 0
    if request.user.is_authenticated:
        #safe gurad if the item is deleted
        try:
            carts = request.user.cart.get() 
            prod = carts.cart_items.get(product=product)
        except:
            prod = None
        
        if prod:
            product_qunatity = prod.quantity

    context = {
        'product': product,
        'qty':product_qunatity
    }
    return render(request, 'product_detail.html', context)

def search(request):
    current_url = request.path_info
    search_results = ''
    if request.GET['search']:
        #get the current search query
        search_string = request.GET['search']
        search_results = Product.objects.filter(name__icontains=search_string)
        
        #update the current path
        current_url += '?search='+search_string

        #info to pass into the html template
        context = {
            'products': search_results,
            'query':search_string,
            'num_result':len(search_results),
            'current_url':current_url
        }
        return render(request,'search_results.html',context)
        
    return redirect(reverse('home'))

def category_list(request, category_name):
    current_url = request.path_info
    
    #get the catergory obj from the db
    category = Category.objects.get(name=category_name)
    
    #get all products in that category
    products = category.items.all()

    #info to pass into the html template
    context = {
        'products':products,
        'category_name':category_name,
        'current_url':current_url,
    }
    return render(request, 'category.html', context)
