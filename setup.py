from setuptools import setup, find_packages
import os

version = __import__('graceful_session_cleanup').__version__

setup(
    name = "django-graceful-session-cleanup",
    version = version,
    url = 'http://github.com/stefanfoulis/django-graceful-session-cleanup',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "A simple management command that can delete expired sessions from large session tables without killing the site.",
    long_description = open('README.rst').read(),
    author = 'Stefan Foulis',
    author_email = 'stefan@foulis.ch',
    packages=find_packages(),
    install_requires = (
        'Django>=1.2,<1.5',
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
