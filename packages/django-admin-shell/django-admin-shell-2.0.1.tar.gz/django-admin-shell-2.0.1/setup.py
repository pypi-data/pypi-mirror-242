# encoding:utf-8
from setuptools import setup, find_packages
from django_admin_shell import __version__ as version


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django-admin-shell',
    version=version,
    description='',
    url='https://github.com/djk2/django-admin-shell',
    author='Grzegorz Tężycki',
    author_email='grzegorz.tezycki@gmail.com',
    long_description=(
        """Django application can execute python code in your """
        """project's environment on django admin site."""
    ),
    license='MIT',
    packages=find_packages(exclude=['docs']),
    package_data={'django_admin_shell': [
        'templates/django_admin_shell/*',
        'static/django_admin_shell/js/*',
        'static/django_admin_shell/js/linedtextarea/*',
        'static/django_admin_shell/fonts/*',
        'static/django_admin_shell/css/*',
    ]},
    tests_require=['Django', 'flake8', 'mock'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=2.0'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
    keywords='django admin shell console terminal',
)
