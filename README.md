# E-market

> Website for buying and selling game account deployed [here](https://buyandplay.herokuapp.com).

* Developed fixtures
  * Login / Registration with email confirm
  * User profile page (with image uploading)
  * CRUD operations via JS
  * Comment model
  * Disqus comments integration
  * Paypal payments integration
  * Stripe payments integration (Card / Bitcoin payments)

## Getting Started

First of all, clone the repo:

```bash
git clone https://github.com/Pavlo-Olshansky/E-market.git
```

## Dependencies
* `django 1.11.2` and `python3`.

## Installing & running
### Dev mode
```
virtualenv venv --no-site-packages
venv/Scripts/activate
pip install -r requirements.txt
```
Then configure your database:
```
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
*Now you can check server at [localhost:8000](http://localhost:8000)*

**Attention : You must run all of these commands in administrator mode**.

## Important note
All env variable is using by `django-decouple` library. System variable in `.env` file are following:
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

## Example
### Comments on home page
#### home.html
```html
<section class="feature">
  <div class="container">
    <div class="row">

    <script type="text/javascript">
      var disqus_config = function () { 
      this.language = "ru";
      };
    </script>

    {% load disqus_tags %}
    {% disqus_dev %}

    <script type="text/javascript">
      var disqus_developer = 1;
      var disqus_url = 'http://buyandplay.com/';
    </script>

    {% load disqus_tags %}
    {% disqus_show_comments %}

    </div>
  </div>
</section>
```


