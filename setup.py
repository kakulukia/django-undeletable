# coding=utf-8
from distutils.core import setup

setup(
    name='django-undeletable',
    packages=['django_undeletable'],  # this must be the same as the name above
    version='0.4.2',
    description='Deleted data stays in the database and will be hidden by default.',
    author='Andy Grabow',
    author_email='andy@freilandkiwis.de',
    url='https://github.com/kakulukia/django-undeletable',  # use the URL to the github repo
    download_url='https://github.com/kakulukia/django-undeletable/tarball/0.4.2',
    keywords=['orm', 'undelete', 'shadow db'],  # arbitrary keywords
    classifiers=[],
    install_requires=['Django>=1.6'],
    license="MIT",
)
