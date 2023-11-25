from setuptools import setup, find_packages

setup(
    name='this_is_my_first_lib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    scripts=[],
    author='Shaheem',
    author_email='shaheemanthony@outlook.com',
    description='A simple hello world lib',
    long_description=open('README.md').read(),
    url='https://github.com/HackerStore/py_lib',
    license='GNU General Public License v3.0',
    zip_safe=False,
)
