Cleave.js integration for Django forms
======================================

This re-usable app helps integrating `Cleave.js`_ into Django projects.
Cleave.js is a JavaScript library that can "help you format input text
content automatically".

`django-cleavejs`_ eases integration into Django. It wraps `Cleave.js`_'s
options object into a form widget class, which takes care of transporting
the options to JavaScript and initialising `Cleave.js`_ for each such
input field.


Installation
------------

To add `django-cleavejs`_ to a project, first add it as dependency to your
project, e.g. using `poetry`_::

  $ poetry add django-cleavejs

Then, add it to your `INSTALLED_APPS` setting to make its static files
available::

  INSTALLED_APPS = [
      ...
      "dj_cleavejs.apps.DjCleaveJSConfig",
      ...
  ]

You need to make `Cleave.js`_ itself available by some means. You can
download it manually, or use your favourite asset management library. For
instance, you could use `django-yarnpkg`_ to depend on the `cleave.js`
Yarn package::

  YARN_INSTALLED_APPS = [
    "cleave.js",
  ]
  NODE_MODULES_ROOT = os.path.join(BASE_DIR, "node_modules")
  STATICFILES_FINDERS += ["django_yarnpkg.finders.NodeModulesFinder"]

You can then either include it in your template yourself, or make
`django-cleavejs`_ add it to its form media by configuring the URL or
path in your settings::

  CLEAVE_JS = "cleave.js/dist/cleave.min.js"

The above example uses the path below `STATIC_ROOT` where `django-yarnpkg`_
would put the package, but you can of course use any URL or path you want
depending on how you want to make `Cleave.js`_ available to the browser.

Usage
-----

Once available, you can create a form as normal and use the widget
on any `CharField`::

  from django.forms import CharField, Form

  from dj_cleavejs import CleaveWidget


  class TestForm(Form):
      windows_xp_serial = CharField(widget=CleaveWidget(blocks=[5, 5, 5, 5, 5],
                              delimiter="-"))

In your template, make sure to include the form media of your form somewhere
**after** the form.

The `CleaveWidget` supports all options `Cleave.js`_ supports, as described
in its `options documentation`_. In the future, `django-cleavejs`_ will also
provide shortcuts.

Example
-------

The source distribution as well as the `Git repository`_ contain a full example
application that serves a test form unter `/test.html`.

It is reduced to a minimal working example for the reader's convenience.

.. _django-cleavejs: https://edugit.org/AlekSIS/libs/django-cleavejs
.. _poetry: https://python-poetry.org/
.. _Cleave.js: https://nosir.github.io/cleave.js/
.. _django-yarnpkg: https://edugit.org/AlekSIS/libs/django-yarnpkg
.. _options documentation: https://github.com/nosir/cleave.js/blob/master/doc/options.md
.. _Git repository: https://edugit.org/AlekSIS/libs/django-cleavejs
