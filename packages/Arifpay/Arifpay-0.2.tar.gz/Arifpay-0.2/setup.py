from setuptools import setup, find_packages

setup(
    name='Arifpay',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'uuid',
        'requests',
        'python-dotenv'
    ],
    author='Ananiya Belew',
    author_email='anewscho@gmail.com',
    description='Create Checkout Session plugin for arifpay',
    url='https://github.com/AnaniyaBelew',
)
