from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required#if we want the user to be login for a view to work
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')


@login_required #Because we put the decorator @login_required, this will ensure that the user is login to logout
def special(request):
    return HttpResponse("You are logged in, Nice")

@login_required #Because we put the decorator @login_required, this will ensure that the user is login to logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))#this will bring back the user to the index Page

def register(request):

    registered=False

    if request.method=="POST": # All this is if the user submit a reques
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()#save the data inside of the database
            user.set_password(user.password) #this hash the password in the database
            user.save()

            profile=profile_form.save(commit=False)# REVIEW WHY HE PUTS THE COMMIT TO FALSE
            profile.user=user# REVIEW THIS PASSAGE

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method=="POST":
        username=request.POST.get('username')#wil go and search for the data inside for the inputs
        password=request.POST.get('password')#wil go and search for the data inside for the inputs

        user=authenticate(username=username,password=password)#this authenticate the data that user have put

        if user:#success with the authentification
            if user.is_active:
                login(request,user)#this will login the user
                return HttpResponseRedirect(reverse('index'))#this will bring back the user to the index Page
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'basic_app/login.html',{})
