from distutils.core import setup

setup(
    name='django-undeletable',
    version='0.1.0',
    author='Andy Grabow	',
    author_email='andy@freilandkiwis.de	',
    packages=['django_undeletable', 'django_undeletable.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/django-undeletable/',
    license='LICENSE.txt',
    description='Deleted data stays in the database and will be hidden from the default manager.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.4",
    ],
)
