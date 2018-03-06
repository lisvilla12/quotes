from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages

def logginuser(request):   
    return User.objects.get(id = request.session['user_id'])

def main(request):
    return render(request, "quote/login.html")

def register(request):
    errorlist = User.objects.validate(request.POST)
    if errorlist[0]:
        hashpw= bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt().encode())
        user=User.objects.create(
            name = request.POST["name"],
            alias = request.POST["alias"],
            email = request.POST["email"],
            password = hashpw,
            birthday = request.POST["birthday"]
            )
        messages.error(request, "Successfully Registered")
        request.session['user_id']= user.id
        return redirect('/main')
    else:
        error = errorlist[1]
        for err in error:
            messages.error(request, err)
        return redirect('/main')

def login(request): 
    user = User.objects.filter(email=request.POST["email"])
    if len(user) > 0:
        user = user[0]
        if bcrypt.checkpw(request.POST["password"].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/quotes')
    else:
        messages.error(request, "invalid login")
        return redirect('/main')
    return redirect('/quotes') 

def quotes(request):
    user = logginuser(request)
    context = {
        "user":user,
        "quotes": Quote.objects.exclude(favorite = user),
        "favorite" : user.favorite.all()
        }
    return render(request,"quote/userpage.html", context)

def create(request):
    errors=Quote.objects.validateQuote(request.POST)
    if errors[0]:
        quote=Quote.objects.create(
            quote = request.POST["quote"],
            quotedby = request.POST["quotedby"],
            user= logginuser(request)
        )
        return redirect('/quotes')
    else:
        error = errors[1]
        for err in error:
            messages.error(request, err)
        return redirect('/quotes')


def addfav(request, id):
    user = logginuser(request)
    favorite = Quote.objects.get(id=id)
    user.favorite.add(favorite)
    return redirect('/quotes')

def removefav(request, id):
    user = logginuser(request)
    favorite = Quote.objects.get(id=id)
    user.favorite.remove(favorite)
    return redirect('/quotes')
        
def users(request, id):
    user=User.objects.get(id=id)
    context = {
        "user":user,
        "quote": Quote.objects.filter(user=id) 
    }
    return render(request, "quote/userinfo.html", context)

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('/main')