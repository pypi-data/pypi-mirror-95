from setuptools import setup

def readme():
	with open('README.md') as f:
		return f.read()


setup(name="primecheck",
	  version='0.0.1',
	  description='Checks if a number is prime or not',
	  long_description=readme(),
	  long_description_content_type='text/markdown',
	  classifiers=[
	  		'Development Status :: 1 - Planning',
	  		'Intended Audience :: Developers',
	  		'License :: OSI Approved :: MIT License',
	  		'Natural Language :: English',
	  		'Operating System :: Microsoft :: Windows',
	  		'Programming Language :: Python :: 3.8',
	  		'Topic :: Scientific/Engineering :: Mathematics'],
	  url='',
	  author='Rayhan',
	  author_email='rayhan.rockz.4.669@gmail.com',
	  keywords='core package',
	  license='MIT',
	  packages=['primecheck'],
	  install_requires=[],
	  include_package_data=True,
	  zip_safe=False)