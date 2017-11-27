# django-knockout-fixture-generator
[![Travis](https://travis-ci.org/skkallayath/django-knockout-fixture-generator.svg?branch=master)](https://travis-ci.org/skkallayath/django-knockout-fixture-generator)
[![License](http://img.shields.io/badge/license-GPLv3-brightgreen.svg?style=flat)](http://www.gnu.org/licenses/gpl-3.0-standalone.html)

Create and manage tournament fixtures (knockout).


The project uses django framework for backend and admin panel and Jquery Brackets to display the fixture.

## Setup

#### Clone the project
```
$ git clone https://github.com/skkallayath/django-knockout-fixture-generator
$ cd django-knockout-fixture-generator
```

#### Create virtual env
```
$ python3 -m virtualenv env
$ source env/bin/activate
```

#### Install packages from requirements.txt
```
(env) $ pip install -r requirement.txt
```

#### Setup databse
```
(env) $ python manage.py migrate
```

#### Create superuser to access admin panel
```
(env) $ python manage.py createsuperuser
```

### Run application

```
(env) $ python manage.py runserver
```


## UI

### Home page

![Home Page](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/fixtures%20ui.PNG)

### Upcoming matches

![Upcoming matches](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/matches%20ui.PNG)

### Fixture

![Fixture](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/fixture%20ui.PNG)


## Admin

Login to `/admin` with the credentials of superuser.

### Add Fixture  

![Add Fixture](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/add%20fixture.PNG)


### Generate Knockout Fixture

![Generate Knockout Fixture](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Generate%20fixture.PNG)

![Generate Knockout Fixture - Message](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Fixture%20generated.PNG)

### Matches of a fixture

![Matches of a fixture](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Matches.PNG)


### Updating match results

![Match results](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Update%20results.PNG)


## About

Mail me to skkallyath@gmail.com


## License

GPL © [Sharafudheen](http://sharafu.in)
