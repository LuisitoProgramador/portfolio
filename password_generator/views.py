from django.shortcuts import render
import random

# Create your views here.

def generator(request):
    return render(request, 'generator_page.html')

def generated(request):
    characters = list('abcdefghijklmnopqrstuvwxyz')
    generated_password = ''

    length = int(request.GET.get('length'))
    uppercase = request.GET.get('uppercase')
    numbers = request.GET.get('numbers')
    special = request.GET.get('special')
    if special:
        characters.extend(list('*+,-./:;<=>?@'))
    if numbers:
        characters.extend(list('1234567890'))
    if uppercase:
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    for _ in range(length):
        generated_password += random.choice(characters)

    return render(request,'generated.html',{
        'password':generated_password,
    })