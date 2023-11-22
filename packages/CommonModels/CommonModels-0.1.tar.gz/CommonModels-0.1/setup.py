from setuptools import setup, find_packages

setup(
    name='CommonModels',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='Shared models for Django microservices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/evercycle-org/common-models',
    author='Evercycle',
    author_email='mija@evercycle.io',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'django>=4.0',
        # Other dependencies, if any
    ],
)