""" A basic script to collect information on Udemy Python courses from a HTML file.

    *This is intended to demonstrate extraction using the BS4 module,
    Udemy actually has an available API which would be the best methods of collection*

    The HTML was collected separately via automation methods and stored in an intermediate file.

"""
from typing import List, Dict
from pathlib import Path
from bs4 import BeautifulSoup
from file_utils import read_text_file, write_json_file

CWD = Path.cwd()
UDEMY_BASE_URL = 'https://udemy.com'
INPUT_HTML_FILE = Path.joinpath(CWD, 'temp_files', 'udemy_python_courses_page_1.html')
OUTPUT_JSON_FILE = Path.joinpath(CWD, 'output_files', 'raw_course_details.json')


def fetch_course_list(soup: BeautifulSoup) -> List[BeautifulSoup]:
    """
    Extract the section of the page source containing the list of courses.
    """
    list_soup = soup.find('div', class_='course-list--container--FuG0T') \
        .findAll('div', class_='popper-module--popper--2BpLn')
    return list_soup


def get_text_section_from_block(soup_section: BeautifulSoup, index: int) -> str:
    """ Extract text from HTML block where the desired content is not separated by logical tags.
    """
    for i, section in enumerate(soup_section.childGenerator()):
        if i == index:
            return section.text


def fetch_course_overview(course_section: BeautifulSoup) -> Dict[str, str]:
    """ Extract the details of a single course and return a dictionary. """
    course_dict = {}
    title_section = course_section.find('h3', {'data-purpose': 'course-title-url'}).find('a')
    course_dict['title'] = get_text_section_from_block(title_section, 0)
    course_dict['course_url'] = f'{UDEMY_BASE_URL}{title_section.get("href")}'
    course_dict['description'] = course_section.find('p', class_='ud-text-sm course-card--course-headline--2DAqq'
                                                     ).text.strip()
    course_dict['instructor'] = course_section.find('div', {'data-purpose':
                                                            'safely-set-inner-html:course-card:visible-instructors'}
                                                    ).text.strip()
    course_dict['rating'] = course_section.find('span', {'data-purpose': 'rating-number'}).text
    course_dict['num_ratings'] = course_section.find('span', class_='ud-text-xs course-card--reviews-text--1yloi').text
    course_metadata = course_section.find('div', {'data-purpose': 'course-meta-info'}).findAll('span')
    course_dict['total_hours_string'] = course_metadata[0].text
    course_dict['num_lectures_string'] = course_metadata[1].text
    course_dict['course_level'] = course_metadata[2].text
    course_dict['current_price_string'] = course_section.find('span', string='Current price').findNext('span').text
    course_dict['original_price_string'] = course_section.find('span', string='Original Price').findNext('span').text
    return course_dict


if __name__ == '__main__':
    udemy_html = read_text_file(INPUT_HTML_FILE)
    udemy_soup = BeautifulSoup(udemy_html, 'html.parser')
    course_list_section = fetch_course_list(udemy_soup)
    course_details = []
    for course in course_list_section:
        course_details.append(fetch_course_overview(course))
    write_json_file(OUTPUT_JSON_FILE, course_details)
