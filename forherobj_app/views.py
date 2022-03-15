from email import message
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

import requests

from .models import WeatherDetails


@login_required(login_url='/login')
def home(request):

    print('------requetd user-----', request.user)
    data = {}
    if request.method == 'POST':
        get_city = request.POST.get('city')

        key = '271d1234d3f497eed5b1d80a07b3fcd1'
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'.format(get_city, key)
        res = requests.get(url).json()
        if res['cod'] == 200:
            
            celsius = (int(res['main']['temp'])-32)*5/9
            try:
                weatherdetail_obj = WeatherDetails.objects.create(city_name=res['name'], longitude=res['coord']['lon'], latitude=res['coord']['lat'], temperature=celsius, country=res['sys']['country'], weather_type=res['weather'][0]['main'], icon=res['weather'][0]['icon'], user_requested=request.user)
                weatherdetail_obj.save()

            except Exception as e:
                print('----exception as e---', e)
                messages.error(request, 'some error internally..')

            data["city_name"]=res['name']
            data["weather"]=res['weather'][0]['main']
            data["temperature"]=celsius
            data['icon'] = res['weather'][0]['icon']
        else:
            messages.error(request, 'The entered city not found..')
    return render(request, 'forherobj_app/home.html', {'data':data})


@login_required(login_url='/login')
def logout(request):
    del request.session['email']
    return redirect('login')


def signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'provided user name already taken..')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Provided Email already taken..')
        else:
            user = User.objects.create_user(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                username=username,
                email=email,
                password=request.POST['password'])
            user.save()
            messages.success(request, 'Register success...')
            return redirect('/')

    return render(request, 'forherobj_app/login.html')


def login_fun(request):
    
    if request.method == 'POST':
        email_input = request.POST.get('email_temp')
        pwd = request.POST.get('pass_temp')

        print('-----email input-------',email_input)
        print('-----pwd input-------',pwd)
        if User.objects.filter(email=email_input).exists():
            user_obj = User.objects.get(email=email_input)
            
            user = authenticate(username=user_obj.username, password=pwd)
            login(request, user)
            print('-------user obj in login------', user)
            if user:
                print('-----inside if user obj and pwd match------')
            #     request.session['email'] = user_obj.email
            #     print('-------request session in login----', request.session['email'])
                messages.success(request, 'You are successfully logged-in.')
                print('------final print of user------', user_obj.username, user_obj.email)
                return redirect('/')
            else:
                print('------pwd mismatch------')
                messages.error(request, 'Password mismatch..!')
        else:
            print('------wrong email----------')
            messages.error(request, 'Please check email..!')
    return render(request, 'forherobj_app/login.html')

