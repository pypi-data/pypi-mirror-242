from pathlib import Path # > 3.6
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf8")

VERSION = '0.0.1'
DESCRIPTION = 'Permite cifrar y descifrar texto'
PACKAGE_NAME = 'onepackage'
AUTHOR = 'Ange1D'
EMAIL = 'ange1d.contact0@gmail.com'
GITHUB_URL = 'https://github.com/Ange1D/ONEPackage'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = [
        'cifrar',
        'descifrar',
        'ONE',
        'Oracle Next Education'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)