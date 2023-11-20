
from setuptools import setup

setup(
    name="compiled",
    version='0.2.0',
    description="Compiled versions of the stdlib.",
    long_description="# compiled\n\nCompiled versions of the stdlib.",
    url="https://github.com/tusharsadhwani/astest",
    author="Tushar Sadhwani",
    author_email="tushar.sadhwani000@gmail.com",
    packages=["compiled"],
    package_data={"compiled": ['difflib.cpython-311-darwin.so', 'fa728a2c4f0df3cb32bd__mypyc.cpython-311-darwin.so', 'tomllib/_parser.cpython-311-darwin.so', 'tomllib/_re.cpython-311-darwin.so', 'tomllib/__init__.cpython-311-darwin.so', 'tomllib/_types.cpython-311-darwin.so']},
    entry_points={
        "console_scripts": ["pycompile=compiled:cli"],
    },
)
