from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from myProject.forms import *
from django.contrib import messages
from myProject.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
import random 
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from myApp.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from notifications.signals import notify


def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('mySigninPage')

    print("account activation: ", account_activation_token.check_token(user, token))

    return redirect('mySigninPage')


def activateEmail(request,user,to_mail):
    mail_sub='Active your user Account'
    message=render_to_string("template_activate.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email= EmailMessage(mail_sub, message, to=[to_mail])
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')

def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            email=form.cleaned_data.get('email')
            activateEmail(request, user,email)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('mySigninPage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signupPage.html', {'form': form})

def mySigninPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashBoardPage')
    else:
        form = AuthenticationForm()
    return render(request, 'loginPage.html', {'form': form})

def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('mySigninPage')

def forget_pass(request):
    if request.method == "POST":
        my_email = request.POST.get("email")
        user = Custom_User.objects.get(email = my_email )
        otp = random.randint(111111,999999)
        user.otp_token = otp
        user.save()
        
        sub = f""" Your OTP : {otp}"""
        msg = f"Your OTP is {otp} , Keep it secret "
        from_mail = EMAIL_HOST_USER
        receipent = [my_email]
        print(user)
        print(receipent)
        print(from_mail)
        
        send_mail(
            subject= sub,
            recipient_list= receipent,
            from_email= from_mail,
            message= msg ,
        )
        return render(request,'updatepass.html',{'email':my_email})

    return render(request, "forgetpass.html")

def update_pass(request):
    if request.method=="POST":
        mail = request.POST.get('email') 
        otp = request.POST.get('otp') 
        password = request.POST.get('password') 
        c_password = request.POST.get('c_password') 
        
        print(mail,otp,password,c_password)

        user = Custom_User.objects.get(email=mail)
        print(user)
        if user.otp_token!= otp :
            return redirect('forget_pass')
        
        if password!= c_password:
            return redirect('forget_pass')
        
        user.set_password(password) 
        user.otp_token = None 
        user.save()
        print(user)
        return redirect ('mySigninPage')

    return render(request, 'updatepass.html')

def dashBoardPage(request):

    return render(request, 'dashBoardPage.html')


def addRecipePage(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            
            notify.send(sender=request.user, recipient=request.user, verb='created', action_object=recipe)
            
            return redirect('viewRecipePage')
    else:
        form = RecipeForm()

    return render(request, 'addRecipePage.html', {'form': form})

def AddRecipeCategoryPage(request):
    if request.method == 'POST':
        form = RecipeCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()  
            notify.send(sender=request.user, recipient=request.user, verb='created', action_object=category)
            return redirect('recipe_categories')
    else:
        form = RecipeCategoryForm()

    return render(request, 'AddRecipeCategoryPage.html', {'form': form})


def recipe_categories(request):
    categories = RecipeCategory.objects.all()
    return render(request, 'recipe_categories.html', {'categories': categories})


def viewRecipePage(request):
    recipes = Recipe.objects.all()
    return render(request, 'viewRecipePage.html', {'recipes': recipes})

def search_results(request):
    query = request.GET.get('query')
    
    recipes = Recipe.objects.filter(
        Q(title__icontains=query) |
        Q(category__name__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

    return render(request, 'search_results.html', {'recipes': recipes, 'query': query})

@login_required
def edit_recipe(request, myid):
    recipe = get_object_or_404(Recipe, id=myid)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('viewRecipePage')
    else:
        form = RecipeForm(instance=recipe)
                                           
    return render(request, 'edit_recipe.html', {'form': form, 'recipe': recipe})

@login_required
def delete_recipe(request, myid):
    recipe = get_object_or_404(Recipe, pk=myid)

    if request.method == 'POST':
        recipe.delete()
        return redirect('view_recipe_page')

    return render(request, 'delete_recipe.html', {'recipe': recipe})

@login_required
def add_to_favorites(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    favorite_recipe, created = FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)

    if created:
        pass
    else:
        pass

    return redirect('viewRecipePage')

@login_required
def view_favorites(request):
    favorite_recipes = FavoriteRecipe.objects.filter(user=request.user)
    return render(request, 'view_favorites.html', {'favorite_recipes': favorite_recipes})

def notifications_page(request):
    
    notifications = request.user.notifications.all()
    notification_count = notifications.count()
    
    context = {
        'notifications': notifications,
        'notification_count': notification_count
    }
    return render(request, 'notifications.html', context)