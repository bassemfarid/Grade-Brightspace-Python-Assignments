"""Lint all student files and write it to a text file."""

import os
import subprocess

# directory possessing all of the student assignments requiring linting
ASSIGNMENTS_DIR = 'assignments'

# Linting options for flake8
# https://flake8.pycqa.org/en/latest/user/options.html
# TODO: Move these options to a separate configuration file
FLAKE8_OPTIONS = [
    '--max-line-length=79',  # default is 79 (PEP 8)
    '--ignore=E123,E126,E133,E226,W503,D205,D400',
    '--disable-noqa',  # In case NOQA is used for silencing
    '--max-doc-length=72',  # PEP 8 standard
    '--statistics',
]


def group_files():
    """Rename and group student files."""
    student_files = {}
    for filename in os.listdir(ASSIGNMENTS_DIR):
        if filename.endswith('.py'):
            if filename.count('-') > 1 or filename.count('_') > 1:
                if '-' in filename:
                    dash_sep_list = filename.split('-')
                    student_name = dash_sep_list[2][1:].replace(' ', '_').lower()
                    new_filename = student_name + '_' + dash_sep_list[4][1:]
                    student_file = os.path.join(ASSIGNMENTS_DIR, filename)
                    new_student_file = os.path.join(ASSIGNMENTS_DIR, new_filename)
                    os.rename(student_file, new_student_file)
                    student_file = new_student_file
                else:
                    student_file = os.path.join(ASSIGNMENTS_DIR, filename)
                    student_name = filename[:filename.rindex('_')]
                if student_name not in student_files:
                    student_files[student_name] = []
                student_files[student_name].append(student_file)
            else:
                student_files[filename] = []
                student_files[filename].append(filename)
    return student_files


def lint_student_files(student_files):
    """Lint all of the student's files using flake8."""
    args = ['flake8'] + FLAKE8_OPTIONS + student_files
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout


def lint_all_students(student_files):
    """Lint all student files."""
    for student in student_files:
        lint_results = lint_student_files(student_files[student])
        output_filename = student + '_lint_results.txt'
        output_file = os.path.join(ASSIGNMENTS_DIR, output_filename)
        with open(output_file, 'w') as f:
            f.write(lint_results)


def main():
    """Run the main script."""
    if not os.path.exists(ASSIGNMENTS_DIR):
        print(f"Error: {ASSIGNMENTS_DIR} directory does not exist")
        return
    student_files = group_files()
    lint_all_students(student_files)


if __name__ == '__main__':
    main()
