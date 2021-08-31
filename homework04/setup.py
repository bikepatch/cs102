import pyvcs
from setuptools import setup

AUTHOR = "Ivan Fomenko"
AUTHOR_EMAIL = "ivanivanfomenko@gmail.com"
HOME_PAGE = "https://github.com/bikepatch/cs102"

setup(
    name="pyvcs",
    version=pyvcs.__version__,
    description="The stupid content tracker",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=["pyvcs"],
    entry_points={"console_scripts": ["pyvcs = pyvcs.__main__:main"]},
    url=HOME_PAGE,
    license="GPLv3",
    python_requires=">=3.6.0",
)
