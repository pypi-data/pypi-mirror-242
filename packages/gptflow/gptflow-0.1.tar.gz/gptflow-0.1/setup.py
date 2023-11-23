
from setuptools import setup, find_packages

setup(
    name='gptflow',
    version='0.1',
    packages=find_packages(),
    description='A brief description of the gptflow package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Artur Grigorev',
    author_email='grigorev.science@gmail.com',
    url='https://github.com/Future-Mobility-Lab/gptflow',
    install_requires=[
        # List XV package dependencies here
        # e.g., 'numpy>=1.18.5',
    ],
)
