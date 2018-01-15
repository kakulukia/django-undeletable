# coding=utf-8
from distutils.core import setup

setup(
    name='django-undeletable',
    packages=['django_undeletable'],
    version='0.5.1',
    description='Deleted data stays in the database and will be hidden by default.',
    author='Andy Grabow',
    author_email='andy@freilandkiwis.de',
    url='https://github.com/kakulukia/django-undeletable',
    download_url='https://github.com/kakulukia/django-undeletable/tarball/0.5.1',
    keywords=['orm', 'undelete', 'shadow db'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['Django>=1.11.8'],
    license="MIT",
)
