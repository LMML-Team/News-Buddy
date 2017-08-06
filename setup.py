from distutils.core import setup
from setuptools import find_packages

try:
    import nltk
except ImportError:
    print("Warning: `nltk` must be installed in order to use `news_buddy`")

try:
     import feedparser
except ImportError:
     print("Warning: `feedparser` must be installed in order to use `news_buddy`")

try:
     import justext
except ImportError:
     print("Warning: `justext` must be installed in order to use `news_buddy`")

try:
     import requests
except ImportError:
     print("Warning: `requests` must be installed in order to use `news_buddy`")


setup(name='news_buddy',
      version='1.0',
      description='Fetches news articles and provides support for entity searches',
      author='Amanda Wang (@CandyMandy28), Anthony Cavallaro (@QuantatativeFinancier), Petar Griggs (@Anonymission), Michael Lai (@impostercafe)',
      author_email="amanda.wang294@gmail.com",
      packages=find_packages(),
      license="MIT"
      )
