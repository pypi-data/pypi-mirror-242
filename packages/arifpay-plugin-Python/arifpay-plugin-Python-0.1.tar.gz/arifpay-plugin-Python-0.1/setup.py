from setuptools import setup, find_packages

setup(
    name='arifpay-plugin-Python',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'uuid',
        'requests',
        'json',
        'python-dotenv'
    ],
    author='Ananiya Belew',
    author_email='anewscho@gmail.com',
    description='Create Checkout Session plugin for arifpay',
    url='https://github.com/AnaniyaBelew',
)
