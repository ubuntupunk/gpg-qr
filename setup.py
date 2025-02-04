from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gpgqr',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'qrcode',
        'requests',
        'Pillow'  # For saving as PNG
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/gpgqr",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'gpgqr = gpgqr.main:main',
        ],
    },
)
