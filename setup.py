from setuptools import setup, find_packages

setup(
      name='robotframework-perfbot',
      version="0.0.1",
      description='Performance Analysis for robot framework',
      long_description='Performance Analysis for robot framework',
      classifiers=[
          'Framework :: Robot Framework',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='robotframework performance',
      author='Lennart Potthoff',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-metrics',
      license='MIT',
      
      packages=find_packages(),
      include_package_data= True,
      zip_safe=False,
      
      install_requires=[
          'robotframework',
          'jinja2',
          'matplotlib',
          'pandas',
          'seaborn'
      ],
      entry_points={
          'console_scripts': [
              'perfbot=perfbot.perfbot:main',
          ]
      },
      )