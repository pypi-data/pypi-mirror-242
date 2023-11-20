from moons import __version__
import os
from setuptools import find_packages, setup
install_requires = [
    'allianceauth>=3.0.0',
    'allianceauth-corptools>=2.5.5',
    'allianceauth-invoices>=0.1.1',
    'django-ninja>=1.0.1,<2.0.0',
]
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='allianceauth-corptools-moons',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    license='MIT',
    description='Alliance Auth Plugin',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/The-Initiative-EvE/allianceauth-corp-tools-moons',
    author='AaronKable',
    author_email='aaronkable@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
