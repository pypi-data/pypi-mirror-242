from setuptools import setup, find_packages

setup(
    name='sage_lib',  # El nombre del paquete
    version='0.1.1.41',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'sage = sage_lib.main:main',  # Establece 'sage' como el comando de consola
        ],
    },
)

