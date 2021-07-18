from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
from django.urls import reverse
from tkinter import Tk, filedialog
import ipywidgets as widgets
import io
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from tqdm.notebook import trange, tqdm
from urllib.parse import urlencode

from .models import UserPreferences
from django.contrib.auth.models import User


class WordCategory:
    def __init__(self, options, name, ans=''):
        self.options_ = options
        self.name_ = name
        self.ans_ = ans


class NumericCategory:
    def __init__(self, mi, ma, i, name, ans=3):
        self.min_ = mi
        self.max_ = ma
        self.mid_ = int((mi + ma + 1) / 2)
        self.id_ = i
        self.name_ = name
        self.ans_ = ans


class Dog:
    def __init__(self, rank, breed, accuracy):
        self.rank_ = rank
        self.breed_ = breed
        self.accuracy_ = accuracy


class Advert:
    def __init__(self, title, price, link):
        self.title_ = title
        self.price_ = price
        self.link_ = link


def registration(request):
    if request.user.id is None:
        context = {
            "logged_in": False,
            "email_taken": False,
        }
    else:
        context = {
            "logged_in": True,
            "user": request.user,
            "email_taken": False,
        }
    if request.method == 'POST':
        first_name = request.POST.get('first_name-name')
        last_name = request.POST.get('last_name-name')
        username = request.POST.get('username-name')
        password = request.POST.get('password-name')
        if User.objects.filter(username=username).exists():
            # bad e-mail, asking to try again
            context.update({
                "email_taken": True,
            })
            return render(request, 'registration.html', context)
        else:
            # everything ok, creating new user
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
        return redirect('/login')
    return render(request, 'registration.html', context)


def ban(request):
    return redirect('/')


def index(request):
    if request.method == 'POST':
        return redirect('adverts/' + request.POST.get('breed'))
    if request.user.id is None:
        context = {"logged_in": False, }
    else:
        if UserPreferences.objects.filter(user=request.user).count() == 0:
            context = {"logged_in": True, "pref_filled": False}
        else:
            context = {"logged_in": True, "pref_filled": True}
            # loading excel file from static files with data about dog breeds
            df = pd.DataFrame(pd.read_excel('staticroot/dogs_data.xlsx'))
            # removing potential missing data
            df.dropna(inplace=True)
            categorical_values = ["Шерстный покров собаки", "Тип поведения", "Аллергия"]
            numerical_values = df.drop(['Порода собаки'] + categorical_values, axis=1)
            # collecting results
            pref = UserPreferences.objects.get(user=request.user)
            cat_results = pref.cat_pref.split('-')
            cat_results.pop()
            num_results = pref.num_pref.split('-')
            num_results.pop()
            num_results = list(map(int, num_results))
            # remove allergic dogs, if user has allergy
            if cat_results[2] == 'нет':
                df = df[df[categorical_values[2]] == 'нет']

            if 'Аллергия' in categorical_values:
                categorical_values.remove('Аллергия')

            total_score = []
            # iterating by rows in dataframe to calculate scores for each breed
            for _, row in df.iterrows():
                res = 0
                for i, value in enumerate(categorical_values):
                    if row[value] == cat_results[i]:
                        # increasing score if selected value equal to value in the row
                        res += 1

                for i, value in enumerate(numerical_values):
                    max_value = df[value].max()
                    # calculating score as (max_value - diff) / max_value
                    score = (max_value - abs(row[value] - num_results[i])) / max_value
                    res += score
                # saving results in list as (breed, accuracy percent)
                total_score.append((row['Порода собаки'], int(res / 11 * 100)))

            # sorting final list
            total_score.sort(key=lambda x: x[1], reverse=True)

            # adding percent sign
            total_score = list(map(lambda x: (x[0], str(x[1]) + '%'), total_score))
            # create dataframe from list
            dog_results = pd.DataFrame(data=total_score, columns=['Breed', 'Accuracy'])
            dog_results.index = np.arange(1, dog_results.shape[0] + 1)

            # picking 5 best dogs for the user
            best_dogs = []
            for rank, row in dog_results.head(5).iterrows():
                best_dogs.append(Dog(rank, row['Breed'], row['Accuracy']))
            context.update({
                "best_dogs": best_dogs,
            })
    return render(request, 'index.html', context)


def preferences(request):
    # loading excel file from static files with data about dog breeds
    df = pd.DataFrame(pd.read_excel('staticroot/dogs_data.xlsx'))
    # removing potential missing data
    df.dropna(inplace=True)
    categorical_values = ["Шерстный покров собаки", "Тип поведения", "Аллергия"]
    numerical_values = df.drop(['Порода собаки'] + categorical_values, axis=1)
    # colors = ['lightblue', 'gold', 'pink', 'lime', 'plum', 'coral', 'turquoise', 'hotpink', 'gold']
    # style = {'description_width': 'initial', 'option_width': 'initial'}

    word_choices = []
    numerical_choices = []

    if UserPreferences.objects.filter(user=request.user).count() == 0:
        context = {"logged_in": True, "pref_filled": False}
        for category in categorical_values:
            options = df[category].unique()
            word = WordCategory(options, category)
            word_choices.append(word)

        # creating choice classes for numerical values
        for i, value in enumerate(numerical_values):
            num = NumericCategory(df[value].min(), df[value].max(), i, value)
            numerical_choices.append(num)
    else:
        pref = UserPreferences.objects.get(user=request.user)
        cat_results = list(pref.cat_pref.split('-'))
        num_results = pref.num_pref.split('-')
        num_results.pop()
        num_results = list(map(int, num_results))
        context = {"logged_in": True, "pref_filled": True}
        for i, category in enumerate(categorical_values):
            options = df[category].unique()
            word = WordCategory(options, category, cat_results[i])
            word_choices.append(word)

        # creating choice classes for numerical values
        for i, value in enumerate(numerical_values):
            num = NumericCategory(df[value].min(), df[value].max(), i, value, num_results[i])
            numerical_choices.append(num)

    # creating choice classes for categorical values

    context.update({
        "word_choices": word_choices,
        "numerical_choices": numerical_choices,
    })

    if request.method == 'POST':
        cat_results = ''
        num_results = ''
        for category in categorical_values:
            cat_results += request.POST.get(category) + '-'
        for value in numerical_values:
            num_results += request.POST.get(value) + '-'
        UserPreferences.objects.filter(user=request.user).delete()
        obj = UserPreferences.objects.create(user=request.user, cat_pref=cat_results, num_pref=num_results)
        obj.save()
        return redirect('/')
    return render(request, 'preferences.html', context)


def parse_data(breed):
    agent = UserAgent(verify_ssl=False).safari
    url = f"https://leboard.ru/ru/moskva/zhivotnye_i_rasteniya/sobaki/?search={breed}"
    response = requests.get(url, {'header': agent})

    # if request was not successful we return empty list
    if response.status_code != 200:
        print("Something went wrong...")
        return []

    tree = BeautifulSoup(response.content, 'html.parser')
    cards = tree.find_all('div', {'class': 'card-post'})

    data = []
    for card in cards:
        link = 'https://leboard.ru' + card.find('a').get('href')
        title = card.find('a').get('title')
        try:
            price = card.find('span', {'itemprop': 'price'}).text + ' руб.'
        except Exception:
            price = 'Цена не указана'
        data.append(Advert(title, price, link))

    return data


def adverts(request, breed):
    if request.user.id is None:
        context = {"logged_in": False, }
    else:
        context = {"logged_in": True, "user": request.user, }

    data = parse_data(breed)
    if len(data) == 0:
        context.update({"found": False})
    else:
        context.update({"found": True, "adverts": data})
    return render(request, 'adverts.html', context)
