from setuptools import setup, find_packages

setup(
    name='crudify',
    version='0.1.0',  # Update with your desired version number
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Your dependencies
        'django',
        'djangorestframework',
        'drf-yasg'
        # Add other dependencies as needed
    ],
)
