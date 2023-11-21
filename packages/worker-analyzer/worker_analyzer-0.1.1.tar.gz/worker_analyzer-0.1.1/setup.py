from setuptools import setup, find_packages

setup(
    name='worker_analyzer',
    version='0.1.1',
    description='Package for analyze and monitoring worker performance',
    author='Claudio Vinicius Oliveira',
    author_email='claudiovinicius.o@hotmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.5,<1.26.0',
        'pandas>=1.1.5,<2.1.0',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'tzdata==2023.3'
    ],
)