# setup.py

from setuptools import setup, find_packages

setup(
    name='myeventstudy',
    version='0.1',
    packages=find_packages(),
    description='Python package for event study analysis',
    author='Qi Yan',
    author_email='953736070@qq.com',
    # url='https://github.com/yourusername/myeventstudy',  # Optional
    install_requires=[
        'pandas',       # pandas library
        'statsmodels',  # statsmodels library
        'scipy'         # scipy library
        # Specify more dependencies as needed
    ],
)
