Live site - http://harga.smach.net/

Getting Started
===============
Make sure to have ``virtualenv``. On Ubuntu, you can install it through ``sudo apt-get install python-virtualenv``. In the root directory::
    
    $ make virtualenv
    $ make requirements
    $ cp harga/example_local_settings.py harga/local_settings.py
    $ # edit database info in local_settings.py
    $ ./bin/python manage.py syncdb
    $ ./bin/python harga/scrape.py <keyword>
    $ ./bin/manage.py rebuild_index
    $ make static # create harga/htdocs dir and run collectstatic command

Deployment
==========
Here's a sample of apache vhost config for deployment with apache using ``mod_wsgi``::

    <VirtualHost *:80>
        ServerName harga.it.cx

        Alias /static /home/kamal/project/harga/harga/htdocs
        <Directory /home/kamal/project/harga/harga/htdocs>
            Order Allow,Deny
            Allow from all
        </Directory>

        WSGIDaemonProcess harga processes=1 threads=10 python-path=/home/kamal/project/harga:/home/kamal/project/harga/lib/python2.7/site-packages
        WSGIProcessGroup harga

        WSGIScriptAlias / /home/kamal/project/harga/harga/wsgi/run.wsgi
    </VirtualHost>

The above assume you checkout the project to ``/home/kamal/project`` when cloning the git repo::

    $ cd /home/kamal/project
    $ git clone git://github.com/k4ml/harga.git

Motivation
==========
http://k4ml.blogspot.com/2012/10/aplikasi-carian-harga-barang-barang.html
