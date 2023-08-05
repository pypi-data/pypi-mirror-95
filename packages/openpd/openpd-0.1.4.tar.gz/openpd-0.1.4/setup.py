from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='openpd',
    version='0.1.4',
    author='Zhenyu Wei',
    author_email='zhenyuwei99@gmail.com',
    description='OpenPD, standing for Open Peptide Dynamics, is a python package for peptide dynamics simulation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='Peptide dynamics simulation package',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://openpd.net/en/latest/',
    project_urls={
        "Documentation": "https://openpd.net/en/latest/",
        "Source Code": "https://github.com/zhenyuwei99/openpd",
    },
    packages=find_packages(), 
    package_data = {
        "data": [
            "*.npy",
            "*.json"
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'numpy',
        'matplotlib',
        'pytest'
    ],
    python_requires='>=3.7'
)
