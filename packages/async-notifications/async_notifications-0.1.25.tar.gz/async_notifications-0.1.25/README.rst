Async notifications
=====================

Email notification with celery and administrative view for send email with delay e.g daily

Features
---------

- Celery integration
- Administrative view 
- Enqueued mail system and instantly send
- Problems notification
- User filter email
- Template system with template context
- Send to User, Group or external email
- Django cms integration (djcms_async_notifications) and standalone.
- Custom text area widget support
- Allow send group mail list if it's defined.
- Newsletter with model context, preview and extra email configuration

Installation
=============

#. Install from pip 

    .. code:: bash
    
        $ pip install async_notifications

#. Add required apps in your settings **

    .. code:: python

        INSTALLED_APPS = [
            ...
            'ajax_select',
            'async_notifications'
        ]

#. Add ajax_select urls in urls.py

    .. code:: python

        from django.conf.urls import url, include
        from ajax_select import urls as ajax_select_urls
        urlpatterns = [
            ...
            url(r'^ajax_select/', include(ajax_select_urls)),
        ]
   
#. It's really important set *CELERY_MODULE* pointing to your project celery file, because it's needed for assing task to the current project, and configure some default celery options

    .. code:: python

        # settings.py
        CELERY_MODULE = "demo.celery"
        CELERY_TIMEZONE = TIME_ZONE
        CELERY_ACCEPT_CONTENT = ['pickle', 'json']
        


#. Configure your email settings, e.g for development

    .. code:: python
    
        DEFAULT_FROM_EMAIL="mail@example.com"
        EMAIL_HOST="localhost"
        EMAIL_PORT="1025"

# Copy celery app in your project folder from demo, and adjust the crontab execution

    .. code:: python

        # celery.py
        app.conf.CELERYBEAT_SCHEDULE = {
            # execute 12:30 pm
            'send_daily_emails': {
                'task': 'async_notifications.tasks.send_daily',
                'schedule': crontab(minute=30, hour=0),

            },
        }

Remember use  demo/__init__.py to update your projectfolder/__init__.py.

#. Run migrations 

    .. code:: bash
    
        $ python manage.py migrate


Runing the project
===================

You need to run 3 subsystems for run this app so you need 3 xterm, for this explanation I will use the demo project

1. Run smtp debug client

    .. code:: bash
    
        $ python -m smtpd -n -c DebuggingServer localhost:1025 

2. Run celery, if you aren't setup celery yet see `celery documentation <http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html>`_.

    .. code:: bash

        $ celery -A demo worker -l info -B
        
3. Run django

    .. code:: bash
    
        $ python manage.py runserver

Usage
=========

Report your context template 

.. code:: python

    from async_notifications.register import update_template_context
    context = [
        ('fieldname', 'Field description'),
        ('fieldname2', 'Field description'),
        ...
    ]
    update_template_context("yourcode",  'your email subject', context )

This automátically create a Email template if not found. 

Context is list of tuples with the fields available in the template context, this context is add in the same file 
that have `send_email_from_template`

Using with django templates 

.. code:: python

    update_template_context("yourcode",  'your email subject', context, 'templatepath.html', as_template=True )

Send dict as context is now available, but remember that you can not repit keys in dict so use with precaution.

Send an email :) 

.. code:: python

    send_email_from_template(code, recipient,
                             context={},
                             enqueued=True,
                             user=None,
                             upfile=None)

Params description:

- `recipient` is a list of emails
- `code` is the same code register in update_template_context
- `enqueued`  if **False** send the email immediately else enqueued to be sent when send email task run.
- `user` user how send email
- `upfile` attached file in email

Other optional options 
========================

Adding context dummy object
----------------------------

When you need to pass a default template message base on template, but you have not the template object
and also you need to write the object with django template sintaxis you can use DummyContextObject that 
return always something like {{ myobj.attr1.objattr }}
    
.. code:: python

    from async_notifications.register import update_template_context, DummyContextObject
    context = [
        ('myobj', 'Field description'),
        ...
    ]
    message = render_to_string('some/template.html',
                           context={
                               'myobj': DummyContextObject('myobj')
                           }
                           )
    update_template_context("yourcode",  'your email subject', context, message=message )


Newsletter email extra configuration
------------------------------------------

As recomendation install django-markitup and markdown to generate preview templates using django template system and configure `ASYNC_NEWSLETTER_WIDGET` to overwrite default text area editor in template newsletter.

If you want to incorporate custom email sender you can configure with `ASYNC_NEWSLETTER_SEVER_CONFIGS`

.. code:: python

    ASYNC_NEWSLETTER_SEVER_CONFIGS={
        'host': 'localhost',
        'port': '1025',
        'fail_silently': False,
        'backend': None,
        'from': 'From user <user@example.com>'
        'username':'my_username',
        'password':'my_password',
        'use_tls': True
    }




Newsletter setup
--------------------

In your app edit at the end of admin.py to register your model


.. code:: python

    register_model('app.model_label', model class, prefix='prefix used to include in template')
    register_news_basemodel('app.model_label', Title, class manager)

To create a new manager you need to create a class like

.. code:: python

    from async_notifications.interfaces import NewsLetterInterface
    class MembershipManager(NewsLetterInterface):
        name = name used to include in template
        model = Model
        form = Filter form class

Take a look to NewsLetterInterface to know what methods you need to overwrite      

Django cms integration
-------------------------

This configuration could help you to integrate with Django CMS.

include in your `INSTALLED_APPS`:

.. code:: python

    INSTALLED_APPS = [
        ...
      'async_notifications',
      'async_notifications.djcms_async_notifications',
    ]

Configure how models and field async_notifications will use, ej. aldryn_people

.. code:: python

    ASYNC_NOTIFICATION_GROUP = 'aldryn_people.Group'
    ASYNC_NOTIFICATION_GROUP_LOOKUP_FIELDS = {
        'order_by': 'translations__name',
        'email': 'email',
        'group_lookup': 'translations__name',
        'display': 'name',
        'filter': ['translations__name__icontains']}


    ASYNC_NOTIFICATION_USER = 'aldryn_people.Person'

    ASYNC_NOTIFICATION_USER_LOOKUP_FIELDS = {
        'order_by': 'translations__name',
        'display': 'name',
        'filter': [
            'user__first_name__icontains',
            'user__last_name__icontains',
            'translations__name__icontains'],
        'group_lookup': 'groups__translations__name'}

.. note:: Django auth is used by default

cmsplugin-contact-plus
-------------------------

CONTACT_PLUS_SEND_METHOD = 'async_notifications.djcms_async_notifications.contact_plus.send_email'
ASYNC_NOTIFICATION_CONTACT_PLUS_EMAIL = 'email'

.. note:: 

    This requires special cmsplugin-contact-plus version, we send a PRs, but is not merged yet.

Default text area widget
--------------------------

For example using ckeditor widget

ASYNC_NOTIFICATION_TEXT_AREA_WIDGET = 'ckeditor.widgets.CKEditorWidget'

.. note:: 
    See how to configure `CKEditor <https://github.com/django-ckeditor/django-ckeditor>`_ .


Extra settings configuration
------------------------------

- ASYNC_NOTIFICATION_MAX_PER_MAIL   default 40 mails per email
- ASYNC_BCC  include always email in BCC comma separed email (without spaces)
- ASYNC_SEND_ONLY_EMAIL  for testing send all email to this address
- ASYNC_SMTP_DEBUG  configure smtp debug for logs
- ASYNC_TEMPLATES_NOTIFICATION   path for save templates created in emails



