from setuptools import setup, find_packages

setup(
    name='idealkr_django_core',
    version='0.1',
    packages=find_packages(),
    description='Django 개발에 유용한 클래스를 포함합니다.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='3chamchi',
    author_email='ceo@idealkr.com',
    url='https://github.com/pro-ideal/idealkr-django-core',
    install_requires=[
        'django>=4.0',  # Specify Django as a dependency
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)