from setuptools import setup, find_packages

setup(
    name='dynamo_db_py',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'schema==0.7.5'
    ]
)
