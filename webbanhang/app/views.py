from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def AddPerson(request):
    Phone = request.POST.get('Phone')
    if Persons.objects.filter(Phone=Phone).exists():
        return HttpResponse("Số điện thoại đã tồn tại")
    else:
        data = {
            'Name' : request.POST.get('Name'),
            'Phone' : request.POST.get('Phone'),
            'Address' : request.POST.get('Address'),
            'DateOfBirth' : request.POST.get('DateOfBirth'),
            'Password' : request.POST.get('Password')
        }
        newPerson = Persons.objects.create(**data)
        request.session['PersonPhone'] = newPerson.Phone
        return redirect('home')
    
def CheckLogin(request):
    Phone = request.POST.get('Phone')
    Password = request.POST.get('PasswordLG')
    try:
        newPerson  = Persons.objects.get(Phone=Phone, Password=Password)
        request.session['PersonPhone'] = newPerson.Phone
        return redirect('home')
    except Persons.DoesNotExist:
        return HttpResponse("Số điện thoại hoặc mật khẩu sai")
    
def home(request):
    newPerson = None
    if Persons.objects.filter(Phone=request.session.get('PersonPhone')).exists():
        newPerson = Persons.objects.get(Phone=request.session.get('PersonPhone'))
    if request.POST.get('PasswordLG'):
        return CheckLogin(request)
    if request.POST.get('Phone'):
        return AddPerson(request)
    count = 0;
    if request.session.get('PersonPhone'):
        booklist = Carts.objects.filter(PersonId = newPerson.Id);
        count = booklist.count();
    books = Books.objects.all()[:6]
    bookssell = Books.objects.order_by('-SellNumber')[:6]
    categories = Categories.objects.all()
    context= {'books': books,'bookssell': bookssell, 'newPerson': newPerson, 'count': count, 'Categories': categories}
    return render(request, 'app/home.html',context)

def bookall(request):
    try:
        Name = request.GET['Name']
        if(Name == '""'):
            Name = ''
        CategoryId = ''
        if request.GET['CategoryId']:
            CategoryId = request.GET['CategoryId']
        if(CategoryId == '""'):
            CategoryId = ''
        CategoryName = "Tất cả"
        if(CategoryId != ''):
            CategoryName = Categories.objects.get(Id = CategoryId).Name
            books = Books.objects.filter(Q(Name__icontains=Name) & Q(CategoryId__exact=CategoryId))
        else:
            books = Books.objects.filter(Q(Name__icontains=Name))
    except Books.DoesNotExist:
        return HttpResponse("Object not found", status=404)
    context= {'books': books, 'CategoryName': CategoryName}
    return render(request, 'app/bookall.html',context)
    

def detail(request):
    try:
        Id = request.GET['Id']
        book = Books.objects.get(Id=Id)
    except Books.DoesNotExist:
        return HttpResponse("Object not found", status=404)
    context= {'book': book}
    return render(request, 'app/detail.html',context)

def cart(request):
    if request.session.get('PersonPhone'):
        person = Persons.objects.get(Phone = request.session.get('PersonPhone'))
        bookscart = Carts.objects.filter(PersonId = person.Id)
        count = 0
        total = 0
        for book in bookscart:
            count += book.Quantity
            total += book.Quantity * book.BookId.Price
        context= {'books': bookscart, 'count': count, 'total': total}
        return render(request, 'app/cart.html',context)
    else:
        return render(request,'app/login.html')
    
def deletebookcart(request):
    person = Persons.objects.get(Phone = request.session.get('PersonPhone'))
    Id = request.GET['Id']
    bookcart = Carts.objects.filter(Id=Id, PersonId=person.Id)
    bookcart.delete()    
    return redirect('cart')

def updatebookcart(request):
    Id = request.GET['Id']
    TT = request.GET['TT']
    person = Persons.objects.get(Phone = request.session.get('PersonPhone'))
    bookcart = Carts.objects.filter(Id=Id, PersonId=person.Id).first()
    if TT == '1':
        bookcart.Quantity +=1
        bookcart.save()
    elif bookcart.Quantity == 1:       
        bookcart.delete()    
    else:
        bookcart.Quantity -=1
        bookcart.save()
    return redirect('cart')

def checkout(request):
    if request.session.get('PersonPhone'):
        Person = Persons.objects.get(Phone = request.session.get('PersonPhone'))
        bookscart = Carts.objects.filter(PersonId = Person.Id)
        count = 0
        total = 0
        for book in bookscart:
            count += book.Quantity
            total += book.Quantity * book.BookId.Price
        context= {'books': bookscart, 'count': count, 'total': total,'person': Person}
        return render(request, 'app/checkout.html',context)
    else:
        return render(request, 'app/login.html')
def Pay(request):
    if request.session.get('PersonPhone') is not None:
        try:
            person = Persons.objects.get(Phone = request.session.get('PersonPhone'))
            booklist = Carts.objects.filter(PersonId = person.Id)
            for item in booklist:
                if Books.objects.get(Id = item.BookId.Id).Quantity - item.Quantity < 0:
                    messages = "Số lượng sách " + item.BookId.Name+ " trong kho không đủ"
                    return HttpResponse(messages)
            for item in booklist:
                book = Books.objects.get(Id = item.BookId.Id)
                book.Quantity -=item.Quantity
                book.SellNumber += item.Quantity
                book.save()               
            booklist.delete()
        except Books.DoesNotExist:
            return HttpResponse("Object not found", status=404)
        return render(request,'app/cart.html')
    else:
        return render(request,'app/login.html')
def register(request):
    return render(request, 'app/register.html')

def login(request):
    return render(request, 'app/login.html')

def logout(request):
    request.session['PersonPhone'] = None
    return render(request, 'app/login.html')

def AddBookCart(request):
    if request.session.get('PersonPhone') is not None:
        try:
            Id = request.GET['Id']
            person = Persons.objects.get(Phone = request.session.get('PersonPhone'))
            if Carts.objects.filter(BookId=Id,PersonId = person.Id).exists():
                bookcart = Carts.objects.get(BookId = Id)
                bookcart.Quantity += 1
                bookcart.save()
            else:
                book = Books.objects.get(Id = Id)
                cart = Carts(PersonId = person,BookId = book,Quantity=1)
                cart.save()
        except Books.DoesNotExist:
            return HttpResponse("Object not found", status=404)
        return redirect('/')
    else:
        return render(request,'app/login.html')
    