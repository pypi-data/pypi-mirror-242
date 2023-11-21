# setup.py

from setuptools import setup, find_packages

setup(
    name='mcbcdc',
    version='0.4',  # Update the version number
    packages=find_packages(),
    include_package_data=True,
    package_data={'file': ['data/*.txt']},
    install_requires=[
        # list your dependencies here
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='Description of your library',
)
