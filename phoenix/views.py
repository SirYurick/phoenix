from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from phoenix.models import Category, Product, Page, UserProfile
from phoenix.forms import UserForm, UserProfileForm


def name_to_url(name):
    return name.replace(' ', '_')
def url_to_name(url):
    return url.replace('_', ' ')

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(title__startswith=starts_with)
    else:
        cat_list = Category.objects.all()

    if max_results > 0 and len(cat_list) > max_results:
        cat_list = cat_list[:max_results]

    for cat in cat_list:
        cat.url = name_to_url(cat.name)
    return cat_list

def get_product_list(category=None, max_results=0):
    product_list = []
    if not category:
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(category=category)
    if max_results:
        if len(product_list) > max_results:
            product_list = product_list[:max_results]

    for product in product_list:
        product.url = name_to_url(product.name)
        if product.multipage:
            product.pages = Page.objects.filter(product=product)
            #print(product, product.pages, '\n')
    return product_list

def index(request):
    cat_list = get_category_list() # For dropdown menu.
    product_list = get_product_list()

    context = {
        'cat_list': cat_list,
        'product_list': product_list,
        }

    if not 'last_visit' in request.session:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    last_visit_time = request.session.get('last_visit')
    date = datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")
    if (datetime.now() - date).days:
        request.session['visits'] += 1
        request.session['last_visit'] = str(datetime.now())

    if 'visits' in request.session:
        context['visits'] = request.session['visits']
    else:
        context['visits'] = 0

    return render(request, 'phoenix/index.html', context)

def category(request, category_url):
    cat_list = get_category_list()
    current_cat = cat_list.get(name=url_to_name(category_url))
    product_list = get_product_list(current_cat)
    for prod in product_list:
        if prod.multipage:
            prod.pages = Page.objects.filter(product=prod)
    context = {
        'cat_list': cat_list,
        'current_cat': current_cat,
        'product_list': product_list,
    }
    return render(request, 'phoenix/category.html', context)

def how_to_buy(request):
    cat_list = get_category_list()
    context = {
    'cat_list': cat_list,
    }
    return render(request, 'phoenix/how_to_buy.html', context)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.bonus = 10
            profile.save()

            registered = True

            login(request, user)
            return render(request, 'phoenix/index.html', {
                'cat_list': get_category_list()
                })
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, render blank form.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'phoenix/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registrered': registered,
        })

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                profile = UserProfile.objects.get(user=user)
                #user.score = profile.score
                return HttpResponseRedirect('/phoenix/')
            else:
                return HttpResponse('Your account is disabled')
        else:
            print('Invalid login details: {0}, {1}'.format(username, password))
            return HttpResponse('Invalid login details supplied')

    else:
        return render(request, 'phoenix/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/phoenix/')

@login_required
def profile(request):
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    return render(request, 'phoenix/profile.html', context_dict)

@login_required
def get_bonus(request):
    user = request.user
    user.userprofile.score += user.userprofile.bonus
    user.userprofile.bonus = 0
    user.userprofile.save()
    return HttpResponse(user.userprofile.score)
