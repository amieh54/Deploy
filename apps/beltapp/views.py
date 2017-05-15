# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

from .models import User, Item, WishList


def index(request):
    return render(request, 'beltapp/index.html')

def regprocess(request):
    result = User.objects.register(request.POST)

    if 'name' in result:
        request.session['action'] = result['action']
        request.session['name'] = result['name']
        return redirect('/dashboard')

    else:
        request.session['errors'] = result
        return redirect('/')

def logprocess(request):
    login = User.objects.login(request.POST)

    if 'action' in login:
        request.session['action'] = login['action']
        request.session['name'] = login['name']
        request.session['id'] = login['user_id']
        return redirect('/dashboard')

    else:
        request.session['logerror'] = login
        return redirect('/')

def logout(request):
        request.session.clear()
        return redirect('/')

def dashboard(request):
    user = User.objects.get(id=request.session['id'])
    mylist = WishList.objects.filter(user=user)
    bottom = Item.objects.exclude(added_by=user)

    context = {
    'mylist': mylist,
    'addeditems': Item.objects.filter(added_by=user),
    'items': Item.objects.exclude(added_by=user),
    'user': user
    }
    return render(request, 'beltapp/dashboard.html', context)

def add_item(request):
    return render(request, 'beltapp/add_item.html')

def items(request):
    user = User.objects.get(id=request.session['id'])
    item = request.POST['item']
    if Item.objects.filter(name=request.POST['item'], added_by=user):
        request.session['message'] = 'You have already added this item.'
        return redirect('/add_item')
    elif len(request.POST['item']) == 0:
        request.session['message']= 'You must enter an item.'
        return redirect('/add_item')
    elif len(request.POST['item']) < 4:
        request.session['message']= 'Item name must be greater than 3 characters.'
        return redirect('/add_item')
    else:
        Item.objects.create(name=request.POST['item'], added_by=user)

        return redirect('/dashboard')

def addwish(request,id):
    WishList.objects.create(user_id=request.session['id'], item_id = id)

    return redirect('/dashboard')

def delete(request,id):
    Item.objects.get(id=id).delete()
    return redirect('/dashboard')

def remove(request,id):
    item = Item.objects.get(id=id)
    user=User.objects.get(id=request.session['id'])
    WishList.objects.filter(item=item, user=user).delete()
    return redirect('/dashboard')

def viewitem(request,id):
    context = {
    'item': Item.objects.get(id=id),
    'list':WishList.objects.filter(item_id=id)
    }
    return render(request, 'beltapp/itempage.html',context)
