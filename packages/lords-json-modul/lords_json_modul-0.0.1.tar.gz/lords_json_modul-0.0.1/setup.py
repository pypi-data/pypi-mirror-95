from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='lords_json_modul',
    version='0.0.1',
    description='A very basic json addon.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Eike Kraus',
    author_email='LordofGamemode@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='json',
    packages=find_packages(),
    install_requires=['json']
)