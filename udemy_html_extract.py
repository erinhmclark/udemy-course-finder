""" A basic scraper to collect information on Udemy Python courses.
    * This is intended to show various methods of extraction, rather than the best method *
    [This site has an underlying API which would be the most efficient method of collection.]
"""
from pathlib import Path
from bs4 import BeautifulSoup

CWD = Path.cwd()
INPUT_HTML_FILE = Path.joinpath(CWD, 'static_files', 'udemy_python_courses_page_1.html')


def read_file(file_path):
    """ Open and read a file. """
    with open(file_path, 'r') as file_obj:
        file_content = file_obj.read()
    return file_content


if __name__ == '__main__':
    udemy_html = read_file(INPUT_HTML_FILE)
    udemy_soup = BeautifulSoup(udemy_html, 'html.parser')
