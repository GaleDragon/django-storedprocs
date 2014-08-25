django-storedprocs
==================

Django App to access, execute, and migrate stored procedures on any database

Why?
====

Stored procedures are awesome and a huge performance boost. Unfortunately, Django doesn't have a means to call a stored procedure in a way that uses its ORM, or a way to migrate them across databases.

That's what this project seeks to remedy.

Installation
============

I haven't gotten around to putting it on PyPI yet, but that's next after this initial smoke test. So for now just install via 

```
git clone https://github.com/GaleDragon/django-storedprocs.git  
cd django-storedprocs  
pip install dist/django-stored-X.Y.tar.gz 
```
or  
`python setup.py install`

After that add this to your INSTALL_APPS:

```
INSTALL_APPS = (
    ...,
    storedprocs,
)
```

and run `./manage.py syncdb --migrate`

You should be installed now!

Usage
=====

Given  
```
class Post(models.Model):
    text = models.CharField(max_length=255)
```

you can do this
```
from storedprocs.models import StoredProcedureManager


class Post(models.Model):
    text = models.CharField(max_length=255)

    objects = models.Manager()
    procedures = StoredProcedureManager()
```

Note that doing this will require an explicit `objects` Manager declaration.  
Or I suppose you could declare `objects` as a `StoredProcedureManager`. Haven't tried that.  

All of the functionality stems from `procedures` fixtures. So in your `fixtures` directory, create a `procedures_X` file, where `X` is the name of your db backend. So you can have separate syntax for a `sqlite3` backend in `procedures_sqlite3` and postgresql syntax in `procedures_postgresql_psychopg2`.

Example:  
```
# procedures_postgresql_psychopg2.json
[{
        "model": "storedprocs.storedprocedure",
        "pk": 1,
        "fields": {
            "attribute": "select_even", # The attribute name you can use on the manager.
            "sql": "FOR row IN SELECT * FROM blog_post WHERE text ~ '(0|2|4|6|8)\\.$';", # The inside of the stored procedure, NOT the function declaration itself.
            "db": "postgresql_psycopg2", # Eventually I want this to determine the db this is loaded on, instead of the file name.
            "primitive": false, # True if the procedure returns a non-queryset (int, str, whatever)
            "primitive_type": "int", # Not needed if primitive == False. Will attempt to cast to this type 
            "return_type": "post" # the model name if primitive == False. This links into the Contenttypes framework.
        }
    }]
```  

Next run the management command `procload`, which will comb fixture directories for procedure files of the default db.

After that, you should be able to use the procedures like  
```
Post.procedures.select_even()
```  
and have it return `Post` objects.


Roadmap
=======

Right now it just works with Sqlite3. I'm busy writing the function templates that each backend will use, starting with PostgrSQL. 
