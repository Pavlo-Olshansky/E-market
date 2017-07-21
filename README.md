# E-market

> Website for buying and selling game account deployed on free host [here](https://buyandplay.herokuapp.com/) 

## Getting Started

First of all, clone the repo:

```bash
git clone https://github.com/Pavlo-Olshansky/E-market.git
cd doctor-appointment
```

## Dependencies
* `django 1.11.2` and `python3`

## Installing & running
### Dev mode
```
virtualenv venv --no-site-packages
venv/Scripts/activate
pip install -r requirements.txt
```
Then configure your database
```
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
*Now you can check server at [localhost:8000](http://localhost:8000)*

**Attention : You must run all of these commands in administrator mode**.

## Important note
All env variable is using by django-decouple library. System variable in .env file are following:
```
ENV_ROLE = development
SECRET_KEY_emarket = <YOUR_SECRET_KEY>
DEBUG = True
DB_PASS_emarket = <YOUR_DB_PASS>
DISQUS_API_KEY=<YOUR_DISQUS_API_KEY>
STRIPE_PUBLISHABLE_KEY=<YOUR_STRIPE_PUBLISHABLE_KEY>
STRIPE_SECRET_KEY=<YOUR_STRIPE_SECRET_KEY>
GMAIL_MAIL=<YOUR_GMAIL_MAIL>
GMAIL_PASS=<YOUR_GMAIL_PASS>
GOOGLE_RECAPTCHA_SECRET_KEY=<YOUR_GOOGLE_RECAPTCHA_SECRET_KEY>
EMAIL_USE_TLS=True
EMAIL_HOST=<YOUR_EMAIL_HOST>
EMAIL_PORT=587
ALLOWED_HOSTS=.localhost, .herokuapp.com
```



