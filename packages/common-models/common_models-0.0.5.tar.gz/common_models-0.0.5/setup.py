from setuptools import setup, find_packages

setup(
    name='common_models',
    version='0.0.5',
    packages=find_packages(),
    description='A package containing common Django eve_models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/evercycle-org/common_models',
    install_requires=[
        'django>=4.0',
    ],
)
