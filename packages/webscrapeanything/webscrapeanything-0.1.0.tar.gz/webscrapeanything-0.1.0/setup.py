from setuptools import setup, find_packages

setup(
    name='webscrapeanything',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'boto3',
        'gspread',
        'oauth2client',
        'pymysql',  # If you're using pymysql in your lambda function for SQL operations
        # other dependencies
    ],
    entry_points={
        'console_scripts': [
            'my_scraper=my_scraper.main:main',
        ],
    },
    package_data={
        # If any package contains *.json files within "templates" directories, include them:
        '': ['templates/*.json'],
    },
    include_package_data=True,  # This tells setuptools to include any data specified in MANIFEST.in
    # Additional metadata like author, description, and so on can be added here
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for web scraping and automation with AWS deployment capabilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # if your README is in markdown
    url='https://github.com/yourusername/webscrapeanything',  # if you have a github repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Based on the libraries and syntax you are using
)
