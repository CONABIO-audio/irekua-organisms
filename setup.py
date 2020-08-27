import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


version = {}
with open("irekua_organisms/version.py") as fp:
    exec(fp.read(), version)


setup(
    name='irekua-organisms',
    version=version['__version__'],
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Irekua model definition for biological organism and specimen storage',
    long_description=README,
    url='https://github.com/CONABIO-audio/irekua-organisms',
    install_requires=['irekua-database'],
    author=(
        'CONABIO, '
        'Gustavo Everardo Robredo Esquivelzeta, '
        'Santiago Martínez Balvanera'),
    author_email='erobredo@conabio.gob.mx, smartinez@conabio.gob.mx',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
