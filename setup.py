from setuptools import setup, find_packages


setup(name='python-snss',
      version="0.1",
      author="Mike Spindel",
      author_email="mike@spindel.is",
      license="MIT",
      keywords="snss chrome session",
      url="http://github.com/deactivated/python-snss",
      description='Parse Google Chrome SNSS files via ',
      install_requires=[
          'construct'
      ],
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Programming Language :: Python"])
