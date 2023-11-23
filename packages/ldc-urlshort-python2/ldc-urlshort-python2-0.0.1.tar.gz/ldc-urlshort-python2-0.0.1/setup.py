from setuptools import setup

setup(
    name='ldc-urlshort-python2',
    version='0.0.1',
    description='A simple package to shorten URLs',
    long_description=open('README.md', 'rb').read(),
    long_description_content_type='text/markdown',
    author='Pratik Kumar',
    author_email='pratik.kumar@lendenclub.com',
    packages=['urlshort_python2', 'urlshort_python2.migrations'],
	classifiers=[
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 2.7",
		"Topic :: Utilities"
	],
    install_requires=[
        'django==1.9.7',
		'djangorestframework==3.5.4',
        'python-dateutil==2.5.3',
    ],
	include_package_data=True
)

