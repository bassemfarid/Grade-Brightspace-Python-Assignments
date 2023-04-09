import os
import subprocess

# directory possessing all of the student assignments requiring linting
ASSIGNMENTS_DIR = 'assignments'

# Linting options for flake8
# https://flake8.pycqa.org/en/latest/user/options.html
FLAKE8_OPTIONS = [
    '--max-line-length=79',  # default is 79
    '--ignore=E123,E126,E133,E226,W503',
    '--disable-noqa',  # In case NOQA is used for silencing
    '--max-doc-length=72',  # PEP suggestion
    '--statistics',
    # '--show-source',
]


def lint_student_file(student_files):
    """Lint all of the student's files using flake8"""
    args = ['flake8'] + FLAKE8_OPTIONS + student_files
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout


def group_files():
    """Rename and group student files"""
    student_files = {}
    for filename in os.listdir(ASSIGNMENTS_DIR):
        if filename.endswith('.py'):
            dash_sep_list = filename.split('-')
            student_name = dash_sep_list[2][1:].replace(' ', '_').lower() + '_'
            if student_name not in student_files:
                student_files[student_name] = []
            new_filename = student_name + dash_sep_list[4][1:]
            new_filename = new_filename
            student_file = os.path.join(ASSIGNMENTS_DIR, filename)
            new_student_file = os.path.join(ASSIGNMENTS_DIR, new_filename)
            os.rename(student_file, new_student_file)
            student_files[student_name].append(new_student_file)
    return student_files


def lint_all_student_files(student_files):
    """
    Lint all student files in the students directory and write the
    results to text files
    """
    for student in student_files:
        lint_results = lint_student_file(student_files[student])
        # Write lint results to text file
        output_filename = student + '_lint_results.txt'
        output_file = os.path.join(ASSIGNMENTS_DIR, output_filename)
        with open(output_file, 'w') as f:
            f.write(lint_results)


def main():
    if not os.path.exists(ASSIGNMENTS_DIR):
        print(f"Error: {ASSIGNMENTS_DIR} directory does not exist")
        return
    student_files = group_files()
    lint_all_student_files(student_files)


if __name__ == '__main__':
    main()
