from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]

setup(name='confiler',
      version='0.1.0',
      author='Vladik Khononov',
      packages=['confiler'],
      install_requires=reqs,
      entry_points={
          'console_scripts': [
              'confiler = confiler.__main__:main'
          ]
      })
      
