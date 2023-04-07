""" Cleaning functions.

Read a file containing scraped Udemy course data, clean and process it, then insert it to an SQLite database.
"""
from pathlib import Path
import logging
from sqlite_utils import Database

from file_utils import read_json_file

CWD = Path.cwd()
RAW_JSON_PATH = Path.joinpath(CWD, 'output_files', 'raw_course_details.json')
CURRENCY_MAP = {'€': 'EUR', '£': 'GBP'}

logging.basicConfig(level=logging.DEBUG)


def get_duration(duration_string):
    """ Convert the string representation of the duration into a datetime object.
    """
    numeric_duration, _, time_measurement = duration_string.split()
    if time_measurement != 'hours':
        logging.warning(f'Unexpected duration format: {duration_string}\n'
                        'Update to process new formats if necessary.')
        return None, None
    return float(numeric_duration), time_measurement


def get_price(price_string):
    """ Get the numeric price and extract the currency.
        Convert the currency to the 3-letter ISO code.
    """
    currency = price_string[:1]
    currency_iso = CURRENCY_MAP.get(currency)
    if not currency_iso:
        logging.warning(f'Unexpected price format: {price_string}'
                        'Update to process new formats if necessary.')
        return None, None
    value = float(price_string[1:])
    return currency_iso, value


def remove_whitespace(text):
    """ Remove excessive whitespace and replace with a single space. """
    text_list = text.replace('/n', ' ').split()
    clean_text = ' '.join([t for t in text_list])
    return clean_text


if __name__ == '__main__':

    json_data = read_json_file(RAW_JSON_PATH)
    if not json_data:
        raise Exception('Input file is empty or failed to load.')

    course_db = Database('course_details.db')
    row_count = len(json_data)
    for i, course in enumerate(json_data):
        course['title'] = remove_whitespace(course.get('title'))
        course['description'] = remove_whitespace(course.get('description'))
        course['total_hours_numeric'], course['duration_type'] = get_duration(course.get('total_hours_string'))
        course['current_currency'], course['current_price'] = get_price(course.get('current_price_string'))
        course['original_currency'], course['original_price'] = get_price(course.get('original_price_string'))

        course_db['topic_details'].insert(course)
        logging.debug(f'Inserted row {i + 1} of {row_count}')

