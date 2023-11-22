from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    readme = f.read()


setup(
    name='m3-python-sdk1',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pika==1.0.0b1',
        'requests==2.31.0',
        'cryptography==41.0.3',
        'boto3==1.26.80',
        'twine==4.0.2'
    ],
    long_description=readme,
    long_description_content_type='text/markdown'
)

# from setuptools import find_packages, setup
#
# setup()
