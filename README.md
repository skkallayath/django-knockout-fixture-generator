# django-knockout-fixture-generator
Create and manage tournament fixtures (knockout).


The project uses django framework for backend and admin panel and Jquery Brackets to display the fixture.

## Setup

Clone the project
```
$ git clone https://github.com/skkallayath/django-knockout-fixture-generator
$ cd django-knockout-fixture-generator
```

Create virtual env
```
$ python3 -m virtualenv env
$ source env/bin/activate
```

Install packages from requirements.txt
```
(env) $ pip install -r requirement.txt
```

Setup databse
```
(env) $ python manage.py migrate
```

Create superuser to access admin panel
```
(env) $ python manage.py createsuperuser
```

## Run application

```
(env) $ python manage.py runserver
```


## Admin

Login to `/admin` with the credentials of superuser.

### Add Fixture  

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/add%20fixture.png)


### Generate Knockout Fixture

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Generate%20fixture.png)

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Fixture%20generated.png)

### Matches of a fixture

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Matches.png)


### Updating match results

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/Update%20results.png)


## UI

### Home page

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/fixtures%20ui.png)

### Upcoming matches

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/matches%20ui.png)

### Fixture

![alt text](https://raw.githubusercontent.com/skkallayath/django-knockout-fixture-generator/master/screenshots/fixture%20ui.png)


## About

Mail me to skkallyath@gmail.com


## License

GPL © [Sharafudheen](http://sharafu.in)
