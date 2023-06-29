from pathlib import Path

UDEMY_BASE_URL = 'https://udemy.com'
CWD = Path.cwd()
TEMP_FILES = Path.joinpath(CWD, 'temp_files')
COOKIE_XPATH = '//button[@id="onetrust-accept-btn-handler"]'
NEXT_PAGE_XPATH = '//a[@aria-label="next page"]'
PAGE_NUM_CLASS = 'ud-heading-sm pagination-module--page--1Ujec'
PAGE_LIMIT = 5


OUTPUT_JSON_FILE = Path.joinpath(CWD, 'output_files', 'raw_course_details.json')
