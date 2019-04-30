from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib import messages
from .models import Restaurant
import pygal
from pygal.style import Style
import numpy as np
import warnings
from collections import Counter
from sklearn import preprocessing, neighbors
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split


import pandas as pd
import random
from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit


weather = YahooWeather(APP_ID="niG5UY74",
                     api_key="dj0yJmk9RW43TFJUdGZkZmdUJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTM3",
                     api_secret="a825085163de09c4ce292e99b575577b3b6a36f1")

weather.get_yahoo_weather_by_city("Vellore", Unit.celsius)

# Create your views here.
def cityselect(request):
	custom_style = Style(
        	background='transparent',
        	plot_background='transparent',
        	opacity = '.5',
        	opacity_hover = '.7',
        	transition = '400ms ease-in',
        	label_font_size = 16,
        	value_font_size = 16,
        	major_label_font_size = 16,
        	legend_font_size = 16,
		#colors = ('#F6b229','#484848', '#E95355', '#E87653', '#E89B53')
        	)
	graph = pygal.Line(style=custom_style,width=700,height=400)
	graph.title = 'Restaurant Weekly Report'
	graph.x_labels = ['Sat','Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
	graph.y_labels = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28]	
	graph.add('Wait time',[2,13,7,17,23,27,24,11],fill=True,dot_size=8)
	graph_data = graph.render_data_uri()

	return render(request,'main/home.html',{"graph_data":graph_data})

def homepage(request, id1):
	#new_restaurant = Restaurant(restaurant_name="Darling Canteen",restaurant_distance="1.5km",restaurant_rating=4,restaurant_wait=15.6)
	#new_restaurant.save()
	return render(request,'main/base.html',{"restaurants":Restaurant.objects.all})

def wait(request, id1, id):
	custom_style = Style(
        	background='transparent',
        	plot_background='transparent',
        	opacity = '.5',
        	opacity_hover = '.7',
        	transition = '400ms ease-in',
        	label_font_size = 16,
        	value_font_size = 16,
        	major_label_font_size = 16,
        	legend_font_size = 16,
		#colors = ('#F6b229','#484848', '#E95355', '#E87653', '#E89B53')
        	)
	obj = Restaurant.objects.get(id=id)
	
	weather_code = [0,0,0,0,0,0,0]
	temperature = [0,0,0,0,0,0,0]
	new_weather = weather.get_forecasts()
	for i in range(0,7):
		weather_code[i] = new_weather[i].code
		temperature[i] = new_weather[i].high


	df = pd.read_csv("H:\Project-Website\mywebapp\main\TRAIN_SET.csv")

	df.drop(['Date'],1,inplace=True)
	df.drop(['Day'],1,inplace=True)

	X = np.array(df.drop(['Realtime'], 1))
	y = np.array(df['Realtime'])

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	clf = neighbors.KNeighborsClassifier()


	clf.fit(X_train, y_train)


	zone = [61,61,61,61,61,61,61]
	coded_day = [2,3,4,5,6,7,1]
	prediction_values=[0,0,0,0,0,0,0]
	for i in range(0,7):	
	    example_measures = np.array([zone[i],coded_day[i],temperature[i],weather_code[i],0])#zone,coded_day,temperture,coded_weather,festive_season
	    example_measures = example_measures.reshape(1, -1)
	    prediction = clf.predict(example_measures)
	    prediction_values[i] = prediction


	graph = pygal.Line(style=custom_style,width=700,height=400)
	graph.title = 'Restaurant Weekly Report'
	graph.x_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
	graph.y_labels = [2,4,6,8,10,12,14,16,18,20,22,24,26,28]	
	graph.add('Wait time',[x[0] for x in prediction_values],fill=True,show_dots=True)
	graph_data = graph.render_data_uri() 

	context = {
		"object": obj,
		"graph_data": graph_data,
	}
	if request.method == "POST":
		new_object = Restaurant.objects.get(id=id)
		new_object.restaurant_queue += 1
		new_object.save()
		return redirect("main:wait", id1=id1, id=id)
 
	return render(request,'main/test.html', context)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    fullname = forms.CharField(label = "First name")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ("username", "fullname", "email", )
   

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.info(request, f"You're logged in as {username}")
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = RegisterForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("main:cityselect")

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect("main:cityselect")
			else:
				messages.error(request,"Invalid username or password")
	form = AuthenticationForm()
	return render(request,
				  "main/login.html",
				  {"form":form})


def shoppage(request, id):
	object = Restaurant.objects.get(id=id)
	if request.method == "POST":
		new_object = Restaurant.objects.get(id=id)
		if(new_object.restaurant_queue != 0):
			new_object.restaurant_queue -= 1
			new_object.save()
			return redirect("main:shoppage", id=id)

	return render(request,"main/shoppage.html",{"object":object})

def aboutSite(request):
	return render(request,"main/about.html")

def requirementNotes(request):
	return render(request,"main/requirementNotes.html")

def policy(request):
	return render(request,"main/policy.html")