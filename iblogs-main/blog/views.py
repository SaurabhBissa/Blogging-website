from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from blog.models import Post, Category


# Create your views here.
def home(request):
    if request.user.is_anonymous:
        return redirect('/Login')
    else:
        # load all the post from db(10)
        posts = Post.objects.all()[:11]
        # print(posts)

        cats = Category.objects.all()

        data = {
            'posts': posts,
            'cats': cats
        }
        return render(request, 'home.html', data)


def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print('username ', username)
        print('password ', password)

        # if user has correct creden...
        user = authenticate(username=username, password=password)
        print('User ', user)

        if user is not None:
            login(request, user)
            # A backend authenticated the credentials
            messages.info(request, 'Login Successful...')
            return redirect('/home')
        else:
            # No backend authenticated the credentials
            messages.info(request, 'Wrong Login Credentials...')
            return render(request, 'login.html')
    else:
        print('POST else')
        return render(request, 'login.html')


def LogoutUser(request):
    messages.info(request,'Logout Successful...')
    logout(request)
    return redirect('/Login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print('username ', username)
        print('email ', email)
        print('password ', password)

        user = User.objects.create_user(username, email, password)
        print('user ', user)

        login(request, user)
        # A backend authenticated the credentials

        messages.info(request, 'Login Successful...')
        return redirect('/home')
        # return render(request, 'home.html')
    else:
        return render(request, 'register.html')



def post(request, url):
    post = Post.objects.get(url=url)
    cats = Category.objects.all()

    # print(post)
    return render(request, 'posts.html', {'post': post, 'cats': cats})


def category(request, url):
    cat = Category.objects.get(url=url)
    posts = Post.objects.filter(cat=cat)
    return render(request, "category.html", {'cat': cat, 'posts': posts})


def about(request):
    return render(request, "about.html")
