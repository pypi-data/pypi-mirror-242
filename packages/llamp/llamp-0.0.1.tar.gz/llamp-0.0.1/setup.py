from setuptools import setup, find_packages

setup(
    name='llamp',
    version='0.0.1',
    description='LLAMP - Large Language Model for Planning',
    author='Nikolai Rozanov',
    author_email='nikolai.rozanov@gmail.com',
    # url='',
    packages=find_packages(include=['llamp']),
    install_requires=[],
    # entry_points={
    #     'console_scripts': ['my-command=exampleproject.example:main']
    # },
    # package_data={'exampleproject': ['data/schema.json']}
)

