####webplay!

##setup (initial)
* [create mySQL db an add info to webplaty/webplay/settings.py]
* source create_virtual_env.sh
* cd webplay/
* python dataman.py --create
* python manage.py syncdb
* python manage.py runserver 0.0.0.0:8000

##setup (non initial)
* source activate_virtual_env.sh
* cd webplay/
* python manage.py runserver 0.0.0.0:8000