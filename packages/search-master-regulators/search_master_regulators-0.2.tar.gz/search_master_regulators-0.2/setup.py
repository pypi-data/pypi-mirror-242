from setuptools import setup, find_packages

setup(
    name='search_master_regulators',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'networkx',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'mycommand = search_master_regulators.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
