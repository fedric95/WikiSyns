# WikiSyns


This module allow people to obtain the list of all the member of a WikiData class and not only their canonical name but also their synonyms.
For example if you would like to obtain the list of all the countries of the world, with this module you would be able to obtain a Pandas Dataframe containing this list with also some of the variants of the country names (ex: USA, United States, ...)

The synonyms of a given name are obtained from the "Also Known As" property in WikiData and the names of the redirects in WikiPedia.


## Requirements for installation from source/github
This module has been tested with Python 3.6.9
All of the required packages can be found on the requirements.txt file.

This module need the access to Internet because it comunicates with the WikiData SparQL Endpoint and the Wikipedia API.

Using pip you can just do this:

git clone https://github.com/fedric95/WikiSyns.git

pip install ./WikiSyns


## Example

-------------------------

git clone https://github.com/fedric95/WikiSyns.git

pip install ./WikiSyns

-------------------------

from WikiSyns.WikiSyns import *

wd = WikidataEntities()

res = wd.get_syns(instancetype='wd:Q5107', language='en')
