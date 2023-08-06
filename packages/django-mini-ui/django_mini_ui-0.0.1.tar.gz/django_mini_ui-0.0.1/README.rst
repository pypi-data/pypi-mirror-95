.. README.rst
Mini
=====

Mini is a reusable Django app to convert text to HTML and apply styles, save code directly to the django's template folder. Also, the HTML code can be downloaded seperately as a html file.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "mini" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mini',
    ]

2. Include the admin & mini URLconf in your project urls.py like this::

	path('admin/', admin.site.urls),
    path('mini/', include('mini.urls')),

3. Run ``python manage.py migrate`` to create the mini models.

4. Start the development server and visit http://127.0.0.1:8000/mini/dashboard
   to start using mini (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/mini/ide to start using the editor.