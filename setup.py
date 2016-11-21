from setuptools import setup, find_packages

setup(name='RTK-handler',
      version='0.2',
      description='UniFE tool that helps in normalization and reconstruction with OpenRTK & SimpleITK.',
      url='https://github.com/dannylessio/RTK-handler',
      author='Danny Lessio',
      author_email='danny.lessio@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[
          'SimpleITK',
          'SimpleRTK',
          'pyexcel',
      ],
      entry_points = {
        'console_scripts': ['RTK-handler=RTK_handler.command_line:main'],
      },
      zip_safe=False)
