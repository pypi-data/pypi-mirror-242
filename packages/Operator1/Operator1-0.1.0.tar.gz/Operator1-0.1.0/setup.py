from setuptools import setup, find_packages

setup(
    name='Operator1',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'apache-airflow>=2.7.3',
    ],
)
