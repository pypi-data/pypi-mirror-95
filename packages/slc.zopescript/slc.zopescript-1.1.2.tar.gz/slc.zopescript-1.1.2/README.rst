.. image:: https://secure.travis-ci.org/syslabcom/slc.zopescript.png
    :target: http://travis-ci.org/#!/syslabcom/slc.zopescript

====================
slc.zopescript
====================

Base classes for running code as Zope console scripts

* `Source code @ GitHub <https://github.com/syslabcom/slc.zopescript>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/slc.zopescript>`_
* `Documentation @ ReadTheDocs <http://slczopescript.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/syslabcom/slc.zopescript>`_

Installation
============

To install `slc.zopescript` you add ``slc.zopescript``
to the dependencies of your own egg.

Usage
=====

slc.zopescript allows running code from the command line with a full Zope
instance and request available.

Console Script
--------------

To create a console script, i.e a script that you can run standalone from a
terminal, you can derive a class from `slc.zopescript.script.ConsoleScript` and
implement the `run()` method. The Zope app will be available as self.app and
the first Plone Site as self.portal.  If you pass a context_path then
self.context will be the object represented by this path; otherwise
self.context will be the portal as well.
A request will be set up so that you can e.g. call browser views.
Example::

    from my.egg import MailHandler
    from slc.zopescript.script import ConsoleScript


    class MailHandlerScript(ConsoleScript):
        def run(self):
            mailhandler_view = MailHandler(self.context, self.context.REQUEST)
            mailhandler_view()

    mail_handler = MailHandlerScript()


In your buildout you can generate the console script e.g. with zc.recipe.egg::

    [mail_handler]
    recipe = zc.recipe.egg
    eggs = ${instance:eggs}
    scripts = mail_handler
    arguments = '${instance:location}/etc/zope.conf','admin',server_url='http://localhost:8081/Plone',context_path='/Plone/news'

The first argument must be the path to a valid zope.conf file. The second
argument is the user to run the script as. The optional server_url should be
the URL under which your site is externally reachable and allows you to use
meaningful absolute_url() calls. The optional context_path is the path to
an object that will be available as self.context in your script class.

Instance Script
---------------

To create an instance script, i.e. a script that you can pass to a zope
instance via `instance run my_script.py`, you can derive a class from
`slc.zopescript.script.InstanceScript` and implement the `run()` method. The
behaviour is similar to ConsoleScript, except that it doesn't set up the app
object but expects it to be passed in when it is instantiated.
Example::

    from my.egg import MailHandler
    from slc.zopescript.script import InstanceScript


    class MailHandlerScript(InstanceScript):
        def run(self):
            mailhandler_view = MailHandler(self.context, self.context.REQUEST)
            mailhandler_view()


    if "app" in locals():
        mail_handler = MailHandlerScript(app)
        mail_handler('admin', server_url='http://localhost:8081/Plone', context_path='/Plone/news')

Save this code as e.g. `mail_handler.py` and call it with `instance run
mail_handler.py`. No buildout configuration is necessary. The arguments for the
call in the last line are the same as the ones you pass in the `arguments`
option for the console script, except that no zope.conf file can be passed.
