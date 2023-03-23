""" A basic script to collect information on Udemy Python courses from a HTML file.
    * This is intended to show various methods of extraction, rather than the best method *
"""
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

CWD = Path.cwd()
INPUT_HTML_FILE = Path.joinpath(CWD, 'static_files', 'udemy_python_courses_page_1.html')
OUTPUT_CSV_FILE = Path.joinpath(CWD, 'output_files', 'raw_course_details.csv')
UDEMY_BASE_URL = 'https://udemy.com'


def read_file(file_path):
    """ Open and read a file. """
    with open(file_path, 'r') as file_obj:
        file_content = file_obj.read()
    return file_content


def fetch_course_list(soup):
    """ Fetch the section of the page source containing the list of courses. """
    list_soup = soup.find('div', class_='course-list--container--FuG0T') \
        .findAll('div', class_='popper-module--popper--2BpLn')
    return list_soup


def get_from_mixed_strings(soup_section, index):
    """ Extract text by index from nested elements,
        and replace excessive whitespace with a single space.
    """
    for i, section in enumerate(soup_section.childGenerator()):
        if i == index:
            text_list = section.text.split()
            clean_text = ' '.join([t for t in text_list])
            return clean_text


def fetch_course_overview(course_section):
    """ Extract the details of a single course and return a dictionary. """
    course_dict = {}
    title_section = course_section.find('h3', {'data-purpose': 'course-title-url'}).find('a')
    course_dict['title'] = get_from_mixed_strings(title_section, 0)
    course_dict['course_url'] = f'{UDEMY_BASE_URL}{title_section.get("href")}'
    course_dict['description'] = course_section.find('p',
                                                     class_='ud-text-sm course-card--course-headline--2DAqq').text.strip()
    course_dict['instructor'] = course_section.find('div',
                                {'data-purpose': 'safely-set-inner-html:course-card:visible-instructors'}).text.strip()
    course_dict['rating'] = course_section.find('span', {'data-purpose': 'rating-number'}).text
    course_dict['num_ratings'] = course_section.find('span', class_='ud-text-xs course-card--reviews-text--1yloi').text
    course_metadata = course_section.find('div', {'data-purpose': 'course-meta-info'}).findAll('span')
    course_dict['total_hours_string'] = course_metadata[0].text
    course_dict['num_lectures_string'] = course_metadata[1].text
    course_dict['course_level'] = course_metadata[2].text
    course_dict['current_price_string'] = course_section.find('span', string='Current price').findNext('span').text
    course_dict['original_price_string'] = course_section.find('span', string='Original Price').findNext('span').text
    return course_dict


def insert_dicts_to_csv(dict_list, csv_path):
    """ Insert a list of Python dictionaries to a csv using the Pandas module. """
    df = pd.DataFrame.from_dict(dict_list)
    df.to_csv(csv_path)


if __name__ == '__main__':
    udemy_html = read_file(INPUT_HTML_FILE)
    udemy_soup = BeautifulSoup(udemy_html, 'html.parser')
    course_list_section = fetch_course_list(udemy_soup)
    course_details = []
    for course in course_list_section:
        course_details.append(fetch_course_overview(course))
    insert_dicts_to_csv(course_details, OUTPUT_CSV_FILE)
