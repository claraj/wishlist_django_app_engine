
useful:
https://cloud.google.com/python/django/flexible-environment

Create project
enable billing

set cmd tool to use this project

```gcloud config set project PROJECT_ID```

settings.py

set allowed hosts in settings to ['*']

app.yaml at same level as mysite and helloworld dirs


new project

```
django-admin start-project mysite
cd mysite
python manage.py startapp hello_world
```

etc.

in terminal

*** DB SETUP ***

enable APIs : cloud SQL api

gcloud  install sql proxy and configure
e.g. on mac: curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64


Create Postgres instance postgres, with strong password
DB user: wishlist_user,  password   

Create database; name matches name given in settings.py

Set local envvars for password, key etc.


# get instance details with
gcloud sql instances describe [YOUR_INSTANCE_NAME]

Start cloud sql proxy, yes with quotes
./cloud_sql_proxy -instances="[YOUR_INSTANCE_CONNECTION_NAME]"=tcp:5432

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wishlist',
        'USER': 'wishlist_user',
        'PASSWORD':  os.getenv('WISHLIST_DB_PW'),
        'PORT': '5432'
    }
}


DATABASES['default']['HOST'] = '/cloudsql/YOUR_INSTANCE_NAME'
if os.getenv('GAE_INSTANCE'):
    pass
else:
    DATABASES['default']['HOST'] = '127.0.0.1'
```



run this to set up tables on cloud server sql
python runserver.py makemigrations
python runserver.py migrate       

*** Static files ***

Create a Cloud Storage bucket.

gsutil mb gs://wishlist-bucket
gsutil defacl set public-read gs://wishlist-bucket

django collect static
set up bucket for static files

in settings.py
STATIC_ROOT = 'static/'
STATIC_URL = 'https://storage.googleapis.com/wishlist-bucket/static/'


# upload to bucket with
gsutil rsync -R static gs://wishlist-bucket/static

```
app.yaml

runtime: python
env: flex
entrypoint: gunicorn -b :$PORT wishlist.wsgi

beta_settings:
  cloud_sql_instances: YOUR_INSTANCE_CONNECTION_STRING

runtime_config:
  python_version: 3
```

And deploy

gcloud app deploy
https://[your instance].appspot.com/


Notes on static files....
https://stackoverflow.com/questions/6014663/django-static-file-not-found
