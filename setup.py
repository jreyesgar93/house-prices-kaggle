from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name = 'house-prices-kaggle',
      version = '0.1',
      description = 'ML Pipleline for the Kaggle House Prices Challence ',
      url = 'https://github.com/jreyesgar93/house-prices-kaggle',
      author = 'Jose Reyes',
      license = 'MIT',
      packages = ['src','utils','pipeline'],
      package_dir={'src':'src','utils':'src/utils','pipeline':'src/pipeline'},
      install_requires = required,
      entry_points ='''
		[console_scripts]
 		houseprices = src.cli2:main
      '''
      )
