from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
from ipywidgets import Button
from tkinter import Tk, filedialog
from IPython.display import clear_output, display
import ipywidgets as widgets
import io
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from tqdm.notebook import trange, tqdm


class WordCategory:
    def __init__(self, options, name):
        self.options_ = options
        self.name_ = name


class NumericCategory:
    def __init__(self, mi, ma, i, name):
        self.min_ = mi
        self.max_ = ma
        self.mid_ = (mi + ma) / 2
        self.box_id_ = i
        self.span_id_ = 10*i
        self.name_ = name


def index(request):
    df = pd.DataFrame(pd.read_excel('staticroot/dogs_data.xlsx'))
    # remove potential missing data
    df.dropna(inplace=True)
    context = {}
    categorical_values = ["Шерстный покров собаки", "Компаньон/Сторожевая/Охотничая", "Аллергия"]
    numerical_values = df.drop(['Порода собаки'] + categorical_values, axis=1)
    # colors = ['lightblue', 'gold', 'pink', 'lime', 'plum', 'coral', 'turquoise', 'hotpink', 'gold']
    # style = {'description_width': 'initial', 'option_width': 'initial'}

    word_choices = []
    numerical_choices = []

    """
    for value in categorical_values:
        options = df[value].unique()
        word = WordCategory(options=options, value=options[0], description=value, style=style)
        word_choices.append(word)
        
    """
    for value in categorical_values:
        options = df[value].unique()
        wid = WordCategory(options, value)
        word_choices.append(wid)

    # show dropdown widgets for categorical values
    for i, value in enumerate(numerical_values):
        num = NumericCategory(df[value].min(), df[value].max(), i, value)
        numerical_choices.append(num)
    context.update({
        "word_choices": word_choices,
        "numerical_choices": numerical_choices,
        "a": "1000",
        "b": "2000",
    })
    if request.method == 'POST':
        return redirect('/results')
    return render(request, 'index.html', context)


def results(request):
    ans = request.POST.get('Аллергия'),
    context = {"ans": ans}
    return render(request, 'results.html', context)
