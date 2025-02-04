from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gpg-qr',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'qrcode',
        'requests',
        'pillow,
           ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/gpg-qr",
    author="David Robert Lewis",
    author_email="ubuntupunk@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'gpg-qr=gpg_qr.main:main',
        ],
    },
    python_requires=">=3.6",
    )
