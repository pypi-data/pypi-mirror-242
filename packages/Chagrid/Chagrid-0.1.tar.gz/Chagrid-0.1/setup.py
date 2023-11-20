from setuptools import setup, find_packages

setup(
    name='Chagrid',
    version='0.1',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    packages=find_packages(),
    install_requires=['CharPackage', 'CharCore', 'gridengine_framework'],
    license='LICENSE.txt',
    description='A package for creating and managing grids of characters.',
    url='https://github.com/primal-coder/Chagrid'
)