from setuptools import setup, find_packages

setup(
    name='ibrokh',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
    author='Ibrokhim Istamov',
    author_email='istamovibrokhim8@gmail.com',
    description='SMS',
    long_description=open('README.md').read(),
    url='https://github.com/Ibrokhim1006/Python-open-sourse.git',
    license='MIT',
)
