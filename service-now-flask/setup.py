from setuptools import setup, find_packages

setup(
    name='service_now_proxy',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)

