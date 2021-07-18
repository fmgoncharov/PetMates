# Проект PetMates

[![made-with-django](https://img.shields.io/badge/made%20with-Django-green)](https://www.djangoproject.com) [![powered-by-leboard](https://img.shields.io/badge/powered%20by-Leboard-informational)](https://leboard.ru)

## 1. Общие положения

**Автор проекта**: Гончаров Фёдор, студент БПМИ202

**Цель проекта**: Разработать и продемонстрировать _web_-приложение, основная задача которого – подбор предложений о продаже собак, на основании предпочтений пользователя

**Используемые библиотеки**: _django_, _bs4_, _requests_, _pandas_, _numpy_, _fake_useragent_

**Описание проекта**: Пользователь регистрируется/авторизовывается на сайте. Далее пользователь на основе собственных предпочтений выбирает длину шёрстного покрова собаки, наличие/отсутсвие аллергии, стоимость содержания, охранные качества, отношение к детям и некоторые другие характеристики, которые он ищет в собаке.

На основании полученных данных, программа предлагает выборку с пятью породами, имеющими наибольшие степени совпадения с предпочтениями пользователя. На следующем шаге пользователь может выбрать понравившуюся собаку, и приложение выведет список предложений о продаже, опубликованных на сайте leabord с комментарием продавца, ценой и активной ссылкой для перехода на сайт.

Понравившееся предложения можно сохранять в избранное и затем просматривать их в профиле. Свои предпочтения можно изменять - соответсвенно будет менятся и набор подходящих вам собак. Про предложенных собак можно узнать детальную информацию и сравнить её со своими предпочтениями, кликнув по названию породы.

## 2. Установка на Linux/Mac

```
git clone https://github.com/fmgoncharov/PetMates
cd PetMates
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 3. Перспективы развития проекта

* Функция нахождения местоположения пользователя - для поиска животного поблизости
* Вывод номера продавца в таблице - для возможности быстрого звонка
* Вывод изображений предлагаемых собак в таблице - для улучшения качества и скорости поиска
* Информация об истории продаж - для предотвращения случаев мошенничества
