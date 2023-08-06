'''
setup.py is the Akasia setup file.
'''

from setuptools import setup

setup(
    version='1.6.0',
    license="MIT License",
    name='Akasia',
    author='Robrecht De Rouck',
    author_email='Robrecht.De.Rouck@gmail.com',
    maintainer='RIDERIUS',
    maintainer_email='riderius.help@gmail.com',
    project_urls={
        "Source Code": "https://github.com/RIDERIUS/Akasia",
        "Documentation": "https://akasia.readthedocs.io/"},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    py_modules=['akasia'],
    entry_points={
        'console_scripts': ['akasia = akasia:main', ], },
    description='A fork tiny python text-based web browser Asiakas.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'beautifulsoup4<=4.9.3',
        'certifi<=2020.12.5',
        'chardet<=4.0.0',
        'dock-python-cli<=0.1.2',
        'dock-python<=0.1.0',
        'html2text<=2020.1.16',
        'idna<=2.10',
        'requests<=2.25.1',
        'soupsieve<=2.2',
        'urllib3<=1.26.3',
        'wikipedia<=1.4.0'
    ]
)
