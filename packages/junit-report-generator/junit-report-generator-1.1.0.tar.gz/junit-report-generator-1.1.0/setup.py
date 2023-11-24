import os
from setuptools import setup, find_packages


files = [os.path.join("templates", "*.css"),
         os.path.join("templates", "*.html")]


setup(
    name="junit-report-generator",
    version="1.1.0",
    description="Generate HTML reports from Junit results",
    author="khoa.dong",
    author_email="dangkhoa0894@gmail.com",
    url="https://your.new.url",
    install_requires=["jinja2>=3.0"],
    packages=find_packages(),
    entry_points={'console_scripts': ['junit-report-generator=junit2htmlreport.runner:start']},
    platforms=["any"],
    license="License :: OSI Approved :: MIT License",
    long_description="Generate a single file HTML report from a Junit or XUnit XML results file"
)