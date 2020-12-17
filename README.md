# getSyns


This module allows people to obtain the list of all the components of a WikiData class and not only their Canonical name but also their synonyms.
For example if I would like to obtain the list of all the countries of the world, with this module I would be able to obtain a Pandas Dataframe containing this list with also some variants of the names (ex: USA, United States, ...)

The synonyms of a given name are obtained from the "Also Known As" property in WikiData and the names of the redirects in Wikipedia.


## Requirements for installation from source/github
This module has been tested with Python 3.6.9
All of the required packages can be found on the requirements.txt file.

Using pip you can just do this:

pip install -r requirements.txt
and it will install all packages from that file
