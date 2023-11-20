from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='AH22CS174',
    version='1.81.12',
    description='A very basic Result calculator',
    long_description='This is a very basic calculator package.',
    url='',
    author='Tanishq JM',
    author_email='tanishqurmi@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='result',
    packages=find_packages(),
    install_requires=['pandas', 'openpyxl']
)
