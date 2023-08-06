from pathlib import Path
from setuptools import setup, find_packages
from os import path

this_dir = path.abspath(path.dirname(__file__))

with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def reqs(file_path):
    with open(Path(file_path)) as fh:
        return [
            r.strip()
            for r in fh.readlines()
            if not (r.startswith("#") or r.startswith("\n"))
        ]


setup(
    name='gretel-core',
    author='Gretel Labs, Inc.',
    author_email='open-source@gretel.ai',
    use_scm_version=True,
    # setup_requires=["setuptools_scm"],
    version="0.1.0",
    description='Balance, anonymize, and share your data. With privacy guarantees.',
    url='https://github.com/gretelai/gretel-core',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires=">=3.6",
    install_requires=reqs("requirements.txt"),
    tests_require=reqs("test-requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
)
