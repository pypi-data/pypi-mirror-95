from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

packages = ['flask_tools']
print('packages=', packages)

setup(
    name="gm_flask_tools",

    version="1.2.6",
    # 1.2.6 - messed up my git repo, i think i fixed it
    packages=packages,
    install_requires=[
        'flask',
        'requests',
    ],

    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A collection of useful tools for developing web pages in python/flask",
    long_description="A collection of useful tools for developing web pages in python/flask",
    license="PSF",
    keywords="grant miller flask tools helpers",
    url="https://github.com/GrantGMiller/gm_flask_tools",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/gm_flask_tools",
    }

    # could also include long_description, download_url, classifiers, etc.
)

# to push to PyPI

# python -m setup.py sdist bdist_wheel
# twine upload dist/*
