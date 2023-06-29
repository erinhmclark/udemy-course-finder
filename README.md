# udemy-course-finder

An example Python script for finding Udemy courses based on user input. 
The script scrapes the Udemy website for course information using Selenium, parses it with beautifulsoup4, and outputs the results to a JSON file. 


## Scraping process

The file `extract_topic_html.py` iterates through the page of results, fetches the html and dumps it into temporary files for later processing.

The file `extract_topic_data.py` extracts content from the HTML stored in the last step:
[https://www.udemy.com/topic/python/](https://www.udemy.com/topic/python/)

The result is then stored in a json file.

The file `clean_topic_data.py` then reads the json file and processes the rows of data, 
cleaning it and formatting fields to the correct data types before inserting it into a SQLite database.

## Requirements

* Python 3.x
* [Poetry](https://python-poetry.org/) for dependency management and packaging.

To install the required libraries clone the project: 

```
git clone https://github.com/erinhmclark/udemy-course-finder.git
```

And run the following commands which change into the project directory and initialise the virtual environment:

```shell
cd udemy-course-finder
poetry init
```

## Improvements

- Add unit tests 
- Add various options to output data to json, csv, etc.
- Add more logs and push these to a log management system
- Insert results into a database, depending on requirements add values such as:
  - timestamps of the date the item was inserted or updated
  - A unique ID for each item
