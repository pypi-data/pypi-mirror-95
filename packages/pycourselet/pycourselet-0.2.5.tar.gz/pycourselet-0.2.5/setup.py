import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements/productive.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="pycourselet",  # Replace with your own username
    version="0.2.5",
    author="Christoph Laßmann",
    author_email="csharplassi@posteo.de",
    description="Tool to create courselets for Lernsax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CsharpLassi/pycourselet",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=required,
    entry_points={
        'console_scripts': [
            'pycourselet = pycourselet.cmd.courselet:run',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
