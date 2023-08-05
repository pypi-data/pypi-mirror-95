import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "gitmiller",
    version = "0.1.5",
    author = "Casper Kaandorp",
    author_email = "c.s.kaandorp@uu.nl",
    description = "A tool to run a Jupyter Notebook from a (partial) Github repository.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/UtrechtUniversity/GitMiller",
    packages = ['gitmiller'],
    entry_points = { 
        'console_scripts': [ 
            'gitmiller = gitmiller.command_line:main'
        ]
    }, 
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires = '>=3.6',
    install_requires = [
        'jupyterlab>=1.2.6',
        'nbformat>=5.1.2',
        'matlab_kernel',
        'papermill',
        'PyGithub>=1.54.1',
        'pyyaml',
        'tqdm'
    ],
)
