#### cpovc_ovc module changes.

> Changes to the code-base of the module from python 2.7 to 3.9

* Refactored the code-base using lib32 python library that converts code from python 2 to 3:

   - upgrades to all python 2.7 syntax

* Refactored code in cpovc_ovc module(Urls,forms,views, and models) to the latest Django 4.0:

    - changes to all imported depreciated django modules and code to latest version in models.py and forms.py.
    - changes to url.py path syntax rendering views from regex format (django 1.8) to latest version in django 4.0
    - changes to all html templates of the cpovc_ovc module that used depraciated format to load static files
    
 > Tests for the models,views and forms
 
 * added tests for models in test.py
  
    - incomplete due to missing :
       - foreign keys
       -  sample data

 * added tests for views in test.py
 
 * addd tests for forms in test.py
 
 > HTMX syntax
 
 	- Added plugin folder for htmx framework in static/plugins/htmx
 	- made changes to base.html :
 		- Added script tag linking base.html to htmx framework in static files
 	- refactored the cpovc_ovc code of all templates to htmx syntax :
 		- Major changes to href -> hx-get for django url and hx-target for html target element(id)
 		 
 		

