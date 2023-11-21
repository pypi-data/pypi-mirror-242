from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()


setup(
    name='web3-authentication-django',
    version='0.3',
    description='A Django app to easily connect web3 authentication to your existing Django projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ahn1305/web3-django-authentication',
    author='Ashwin B',
    author_email='ahnashwin1305@gmail.com',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    package_data={
        '': ['*.md'],
    },
)
