# udemy-course-finder

An example scraper project which collects course information from Udemy.

# Process

The first thing to check when making a scraper is to check the site's robots.txt:
[https://www.udemy.com/robots.txt](https://www.udemy.com/robots.txt)
This does not disallow the topic path (at this point in time), so I chose this as an example to use. 
Note that this does not mean these paths are impossible to get programmatically, it is an indication for search engines, 
but also means they are politely asking you to not automate it, at least not to spam it.
Using Selenium with Chrome worked for me (with a couple of extra configurations added!) 
however I am not publishing that script publicly as there were bot detections mesures that the extraction needed to get around.


## Version 0.1

The file `extract_topic_data.py` mimics a simplified scraper by extracting content from some pre-stored HTML from the URL:
[https://www.udemy.com/topic/python/](https://www.udemy.com/topic/python/)

The result is then stored (in its basic format) in a json file.

The file `clean_topic_data.py` then reads the json file and processes the rows of data, 
cleaning it and formatting fields to the correct data types before inserting it into a SQLite database.

## Requirements

* Python 3.x
* [Poetry](https://python-poetry.org/) for dependency management and packaging.

To install the required libraries clone the project and run the following commands:

```shell
cd udemy-course-finder
poetry init
```

## Improvements

- Add unit tests 
- Add various options to output data to json, csv, etc.
- Create custom loggers and log these to a log management system
- Extract global variables to configuration file where they can be easily modified
- Create a more substantial database, depending on requirements add values such as:
  - timestamps of the date the item was inserted or updated
  - A unique ID for each item
