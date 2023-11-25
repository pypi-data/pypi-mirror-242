from setuptools import setup

__project__ = 'mcpi_listener'
__desc__ = 'Python library for the Minecraft Pi edition and RaspberryJuice API'
__version__ = '1.0.1'
__author__ = "Barbashin Andrey"
__author_email__ = 'barbashin.andrey@vk.com'
__url__ = 'https://github.com/barbashin-andrey/mcpi-listener'
__long_description__ = '# Package for listening to the minecraft events (uses MCPI)'

__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: Games/Entertainment",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

__install_requires__=[
    'mcpi',
]

setup(name=__project__,
      version = __version__,
      description = __desc__,
      long_description=__long_description__,
      long_description_content_type='text/markdown',
      url = __url__,
      author = __author__,
      author_email = __author_email__,
      packages = [__project__],
      classifiers = __classifiers__,
      zip_safe=False,
      install_requires = __install_requires__)