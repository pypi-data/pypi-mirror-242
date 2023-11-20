
from setuptools import setup, find_packages

from mypyc.build import mypycify

setup(
    name="compiled",
    version='0.2.1',
    description="Compiled versions of the stdlib.",
    long_description="# compiled\n\nCompiled versions of the stdlib.",
    url="https://github.com/tusharsadhwani/compiled",
    author="Tushar Sadhwani",
    author_email="tushar.sadhwani000@gmail.com",
    packages=find_packages(),
    ext_modules=mypycify(["--strict", *['compiled/difflib.py', 'compiled/tomllib/_types.py', 'compiled/tomllib/__init__.py', 'compiled/tomllib/_parser.py', 'compiled/tomllib/_re.py']]),
    entry_points={
        "console_scripts": ["pycompile=compiled:cli"],
    },
)
