# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


requirements = [
    "numpy>=1.20.1",
    "setuptools~=53.0.0",
    "pytz>=2021.1",
    "nose>=1.3.7",
    "opencv-python>=4.5.1.48",
    "click>=7.1.2",
    "requests>=2.25.1",
    "PyPDF2>=1.26.0",
    "Pillow>=8.1.0",
    "pdf2image>=1.14.0",
    "pytesseract>=0.3.7",
]

setup_requirements = []


test_requirements = []

setup(
    name='ocr-joplin-notes',
    version='0.2.1',
    description='Add OCR data to Joplin notes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Matthijs Dekker',
    author_email='joplin-development@dekkr.nl',
    url='https://github.com/plamola/ocr-joplin-notes',
    install_requires=requirements,
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    keywords=["ocr-joplin-notes", "joplin", "ocr-joplin-notes"],
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    python_requires=">=3.5",
)

