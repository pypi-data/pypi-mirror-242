from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='DjangoCRUDify',
    version='0.3.0',
    author='Anshu Pal',
    author_email='anshupal257@gmail.com',
    description='DjangoCRUDify is a powerful and intuitive Django app that automates the generation of CRUD (Create, Read, Update, Delete) APIs for your Django models. With minimal configuration, turn your existing models into a fully functional API, complete with Swagger documentation for seamless integration.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/anshuUnity/DjangoCRUDify',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        # Your dependencies here
        'Django',
        'djangorestframework',
        'drf-yasg'
    ],
    include_package_data=True,
    package_data={'': ['LICENSE']},
    license_files=('LICENSE',),
)
