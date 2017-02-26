from setuptools import setup

setup(name='confiler',
      version='0.1.0',
      author='Vladik Khononov',
      packages=['confiler'],
      entry_points={
          'console_scripts': [
              'confiler = confiler.__main__:main'
          ]
      })
      
