"""Lint all student files and write it to a text file."""

import os
import subprocess

import dropboxtools

# Directory possessing all of the student assignments requiring linting
ASSIGNMENTS_DIR = 'assignments'

# TODO: Should linter be transitioned to RUFF?
# Linting options for flake8
# https://flake8.pycqa.org/en/latest/user/options.html
# TODO: Move these options to a separate configuration file
FLAKE8_OPTIONS = [
    '--max-line-length=79',  # default is 79 (PEP 8)
    '--ignore=E123,E126,E133,E226,W503,D205,D400',
    '--disable-noqa',  # In case NOQA is used for silencing
    '--max-doc-length=72'  # PEP 8 standard
]

FLAKE8_STAT_OPTIONS = FLAKE8_OPTIONS + ['--quiet', '--statistics']

FLAKE8_VERSION = subprocess.run(
    ['flake8', '--version'], capture_output=True, text=True).stdout


def get_new_filename(file_meta: dict) -> str:
    """Generate new name from Dropbox file meta data.

    Args:
        file_meta (dict): dictionary of dropbox file meta data

    Returns:
        str: New formatted filename
    """
    new_filename = (f"{file_meta['student_name']} - {file_meta['filename']}."
                    + file_meta['file_extension'])
    return new_filename


def rename_file(old_filename: str, new_filename: str) -> None:
    """Rename Dropbox file into an easier format.

    Args:
        old_filename (str): The old file name
        new_filename (str): The new formatted file name
    """
    old_file = os.path.join(ASSIGNMENTS_DIR, old_filename)
    new_file = os.path.join(ASSIGNMENTS_DIR, new_filename)
    os.rename(old_file, new_file)


def group_files() -> dict[str, list[str]]:
    """Rename and group student files."""
    students_files = {}
    for filename in os.listdir(ASSIGNMENTS_DIR):
        if filename.endswith('.py'):

            if dropboxtools.file_check(filename):
                file_meta = dropboxtools.get_file_details(filename)
                student_name = file_meta['student_name']
                new_filename = get_new_filename(file_meta)
                rename_file(filename, new_filename)

            else:
                new_filename = filename

                # Below will incorrectly assume beginning of file is
                # the student_name, grouping it as such in
                # students_files
                if ' - ' in new_filename:
                    student_name = new_filename[:new_filename.index(' - ')]
                else:
                    student_name = new_filename

            student_file = os.path.join(ASSIGNMENTS_DIR, new_filename)

            if student_name not in students_files:
                students_files[student_name] = []
            students_files[student_name].append(student_file)

    return students_files


def lint_student_files(student_name: str, student_files: list[str]) -> str:
    """Lint all of the student's files using flake8."""
    stat_args = ['flake8'] + FLAKE8_STAT_OPTIONS + student_files
    stat_results = subprocess.run(
        stat_args, capture_output=True, text=True).stdout

    args = ['flake8'] + FLAKE8_OPTIONS + student_files
    result = subprocess.run(args, capture_output=True, text=True).stdout

    intro_msg = f"Below are a list of problems with the formatting of your program according to PEP 8 standards. This has an effect on your communication and knowledge categories. To generate this list, The following flake8 version was used along with their extensions.\n{FLAKE8_VERSION}"  # NOQA

    file_string = intro_msg + '\n--Files and Overall Stats--\n' + \
        stat_results + '\n--Detailed Results--\n' + result
    file_prefix = os.path.join(ASSIGNMENTS_DIR, student_name + ' - ')
    file_string = file_string.replace(file_prefix, '')

    return file_string


def lint_all_students(students_files: dict[str, list[str]]) -> None:
    """Lint all student files."""
    for student in students_files:
        lint_results = lint_student_files(student, students_files[student])
        output_filename = student + '_lint_results.txt'
        output_file = os.path.join(ASSIGNMENTS_DIR, output_filename)
        with open(output_file, 'w') as f:
            f.write(lint_results)


def main():
    """Run the main script."""
    if not os.path.exists(ASSIGNMENTS_DIR):
        print(f"Error: {ASSIGNMENTS_DIR} directory does not exist")
        return
    students_files = group_files()
    lint_all_students(students_files)


if __name__ == '__main__':
    main()
