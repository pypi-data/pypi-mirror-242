from setuptools import setup, find_packages
from trix_widget.version import Version


setup(name='django-trix-widget',
     version=Version('1.0.0').number,
     description='Trix widget for Django',
     long_description=open('README.md').read().strip(),
     long_description_content_type="text/markdown",
     author='Bram Boogaard',
     author_email='padawan@hetnet.nl',
     url='https://github.com/bboogaard/django-trix-widget',
     packages=find_packages(include=['trix_widget']),
     install_requires=[
         'pytest',
         'pytest-cov',
         'pytest-django==4.5.2',
         'django==4.2.7',
         'pyquery==2.0.0',
         'bleach==6.1.0'
     ],
     license='MIT License',
     zip_safe=False,
     keywords='Django Trix widget',
     classifiers=['Development Status :: 3 - Alpha'])
