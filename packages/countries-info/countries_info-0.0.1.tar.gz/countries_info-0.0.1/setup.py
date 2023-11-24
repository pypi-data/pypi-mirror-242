from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'Simple library to get information about country'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="countries_info",
    version=VERSION,
    author="iqballl",
    author_email="<rafiiqbal2407@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/iqbull2244/negara',
    packages=find_packages(),
    install_requires=[],
    keywords=['countries', 'negara'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)