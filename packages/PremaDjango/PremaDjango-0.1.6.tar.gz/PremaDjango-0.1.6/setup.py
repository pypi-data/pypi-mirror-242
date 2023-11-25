# from setuptools import setup, find_packages
#
# setup(
#     name='PremaDjango',
#     use_scm_version=True,
#     setup_requires=['setuptools_scm'],
#     packages=find_packages(),
#     install_requires=[
#         # List your dependencies here
#     ],
# )
#

from setuptools import setup, find_packages

setup(
    name='PremaDjango',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'Django',  # Add other default libraries here
    ],
)