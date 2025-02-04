from setuptools import setup, find_packages

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
    entry_points={
        'console_scripts': [
            'gpgqr = gpgqr.main:main',
        ],
    },
)
