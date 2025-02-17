from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gpg-qrcode',
    version='0.1.3',
    summary='A tool for generating qr codes from gpg certificates',
    description='A tool for generating qr-codes from gpg ascii keys and revoke certificates',
    license_file="LICENSE",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'qrcode',
        'requests',
        'pillow',
           ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/gpg-qrcode",
    author="David Robert Lewis",
    author_email="ubuntupunk@gmail.com",
    keywords='revoke, gpg, qrcode',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'gpg-qrcode=gpg_qr.main:main',
        ],
    },
    python_requires=">=3.6",
    )
