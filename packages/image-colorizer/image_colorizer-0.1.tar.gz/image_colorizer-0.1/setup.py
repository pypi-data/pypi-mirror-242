
from setuptools import setup, find_packages

setup(
    name='image_colorizer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'fastai',
        'Pillow',  # PIL
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='An image colorization package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
