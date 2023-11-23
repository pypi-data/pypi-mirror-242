# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='myeventstudy',
    version='0.1.4',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={'': ['README.md']},
    description='Python package for event study analysis',
    author='Qi Yan',
    author_email='953736070@qq.com',
    url='https://pypi.org/project/myeventstudy/',  # Optional
    license='MIT',
    install_requires=[
        'pandas',       # pandas library
        'statsmodels',  # statsmodels library
        'scipy'         # scipy library
        # Specify more dependencies as needed
    ],
)
