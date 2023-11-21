from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Python wrapper of R package `iglu` for continuous glucose monitoring data analysis. Wraps the R functions, thus making them accessible in Python.'

# Setting up
setup(
        name='iglu-r', # name must match the folder name where code lives
        version=VERSION,
        author='Lizzie Chun, Nathaniel J. Fernandes, Irina Gaynanova',
        author_email='lizzie_chun1@tamu.edu, njfernandes24@tamu.edu, irinagn@umich.edu', 
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['rpy2>=3.5.13', 'pandas>=2.1.2'], # we've validated functionality with these package versions.     
        keywords=['iglu', 'Continuous Glucose Monitoring analysis software', 'diabetes'],
        include_package_data=True
)