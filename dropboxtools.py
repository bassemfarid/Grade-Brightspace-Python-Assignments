"""Tools to provide an interface for Brightspace Dropbox."""

import re

FILENAME_PATTERN = re.compile(
    r'(?P<student_id>\d+)-'
    + r'(?P<dp_id>\d+) '
    + r'- (?P<student_name>[\w\s]+)'
    + r'- (?P<date_time>[\w\s,]+) '
    + r'- (?P<filename>.+)'
)
FILE_EXTENSION_PATTERN = re.compile(r'(.+)\.(.+)')


def file_check(filename: str) -> bool:
    """Check if provided filename is of Dropbox format.

    Args:
        filename (str): Name of the file.

    Returns:
        bool: True if in Dropbox format else False.
    """
    return FILENAME_PATTERN.fullmatch(filename) is not None


def get_file_details(filename: str) -> dict:
    """Get the Brightspace meta details of the file.

    Args:
        filename (str): valid dropbox file name

    Returns:
        dict: student_id, dp_id, student_name, date_time, filename,
              and file_extension
    """
    m = FILENAME_PATTERN.fullmatch(filename)
    m_dict = m.groupdict()
    m_dict['file_extension'] = None
    file_ext_match = FILE_EXTENSION_PATTERN.fullmatch(m_dict['filename'])
    if file_ext_match:
        m_dict['filename'] = file_ext_match.group(1)
        m_dict['file_extension'] = file_ext_match.group(2)
    return m_dict
