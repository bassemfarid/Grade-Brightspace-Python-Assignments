# Generate Linting Feedback for Python Assignments Submitted to Brightspace Dropbox

## Purpose

This project attempts to ease grading Python assignments from Brightspace by using packages to enforce standards and bulk generating *some* feedback and grades.

The project mainly uses Flake8 that exercises multiple extensions and plugins to check for various standards. 

### Standards
This project uses common standards for Python, which were provided to students in a marking scheme.
#### Styling
[PEP 8](https://peps.python.org/pep-0008/) is the standard that will be used for grading styling. To check for some of these standards, Flake8 uses pycodestyle.


## Usage
1. Install required packages using `pip install -r requirements.txt`.
2. Brightspace: bulk download all the assignments submitted in the assignment folder submission by checking off 'select all rows' and clicking download. Extract all the files into the `assignments` folder at the same location as the script.
3. Run the lint_files script.