import os
from setuptools import setup, find_packages
from standingsrequests import __version__

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="aa-standingsrequests",
    version=__version__,
    description=(
        "App for managing character standing requests, made for Alliance Auth"
    ),
    url="https://gitlab.com/basraah/standingsrequests",
    author="Basraah, Erik Kalkoken",
    author_email="kaloken87@gmail.com",
    license="GPL-3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires="~=3.6",
    install_requires=[
        "allianceauth>=2.8.1",
        "django-esi>=1.5<3",
        "requests>=2.18.4",
        "allianceauth-app-utils>=1.0.0",
    ],
)
