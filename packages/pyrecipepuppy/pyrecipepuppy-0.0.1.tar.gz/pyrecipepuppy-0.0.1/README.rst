**pyrecipepuppy**

A simple Python wrapper for the *Recipe Puppy API*

Makes requests to the Recipe Puppy API to retrieve the recipes containing a given list
of ingredients and/or a given search term. It returns the list of all the
recipes returned by the API. For each recipe the following data might
be available:

* title
* link to a web page containing the entire recipe
* the list of ingredients used in the recipe
* link to a thumbnail photo with the result of the recipe

For more information on the API, please visit the `Recipe Puppy API web page <http://www.recipepuppy.com/about/api/>`_

**Installation**

``pip install pyrecipepuppy``

**Usage**::

    import pprint
    from pyrecipepuppy import RecipePuppy

    rp = RecipePuppy()
    recipes = rp.get_recipes(ingredients='salmon,onions', search_query='omelet')
    pprint.pprint(recipes)

