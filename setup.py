from setuptools import setup, find_packages

setup(
      name='perfbot',
      version="1.0.0",
      description='Perfbot',
      long_description='Performance Analysis for Robot Framework',
      classifiers=[
          'Framework :: Robot Framework',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='robotframework performance',
      author='Lennart Potthoff',
      author_email='git@circuit-break.in',
      url='https://github.com/perfroboter/robotframework-perfbot',
     license = 'MIT',
      
      packages=find_packages(),
      include_package_data= True,
      zip_safe=False,
      
      install_requires=[
          'robotframework',
          #'jinja2', # Only for robotmetrics-Extension
          'matplotlib',
          'pandas',
          'seaborn'
      ],
      entry_points={
          'console_scripts': [
              'perfbot=perfbot.perfbot:main'
          ]
      },
      test_suite="perfbot.tests",
      )
