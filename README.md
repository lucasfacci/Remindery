# Remindery

## Distinctiveness and Complexity

This project is called Remindery, it's a calendars website made using Django on the back-end and Javascript on the front-end. This projects satisfies all the distinctiveness and complexity requirements, because it's a totally different idea from the other projects in this course.

The idea behind Remindery, is to be a calendars website where the users can create reminders of everyday tasks. Once logged in the website, it's possible to create calendars and share this it to other users too, this way the user can have a personal or a shared calendar.

The distinctiveness of this project from the others is very clear, since it doesn't appear to be a social network, an e-commerce or an e-mail, and it's not based on the old CS50W Pizza project. It's completely different from the other projects in the course too, that even used Javascript in the front-end.

It's possible to check the project complexity in relation to the other ones, once it has much more functions compared to the others. It also included some models and it's completely mobile-responsive.

## Project Files

There's not many additional files that I created beyond the Django framework standards. But inside the static directory there's some Bootstrap files, used to assist in the website responsiveness, but beyond these, there's my own custom CSS and Javascript files, one called "styles.css" and the other "scripts.js", and there's some SVG images that I used in the project too. And inside the templates directory in the reminder app there's all the HTML files used in the website.

In the "styles.css" file, there is some classes that I created to turn possible to do some things Bootstrap itself didn't allowed exactly the way I wanted. One of the those that worth to highlight is the one that used keyframes to enable the clouds animation when entering in the website. And in the "scripts.js" file, there's all the Javascript front-end used in the project, that is possible to interact after logged in.

Inside the reminder app in the templates folder, there's the "layout.html" that is the parent HTML file, and all the others inherit from it. The "index.html" is the first page that is seen when the website is accessed, and from it is possible to access the "register.html" page, where the user can make an account, and the "login.html" page, where the user can login in the account. After logging in, the user is presented with the "main.html" page, where the custom "scripts.js" file interacts with.

## How to run the application

First of all, it's necessary to generate a new Django secret key with the code bellow:

```
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```

After that it's necessary to create a config.py file at the root of the project with a variable called KEY and the value being the random key that you previously generated, for example ```KEY = 'THE GENERATED SECRET KEY GOES HERE'```. After you did these steps, you can follow the commands bellow to initialize the application. :)

### Linux

```
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

### Windows

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Additional information

### Troubleshooting

If having problemm with any of the commands on the "How to run the application" section, try 'python3' instead of 'python' and/or 'pip3' instead of 'pip'.
