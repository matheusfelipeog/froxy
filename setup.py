# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='froxy',
    version='1.0.1',
    description='Hide your IP with free proxies using Froxy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Matheus Felipe',
    author_email='matheusfelipeog@gmail.com',
    url='https://github.com/matheusfelipeog/froxy',
    packages=find_packages(),
    install_requires=['requests'],
    zip_safe=False,
    python_requires='>=3.6',
    project_urls={
        "Bug Tracker": "https://github.com/matheusfelipeog/froxy/issues",
        "Documentation": "https://github.com/matheusfelipeog/froxy/blob/master/README.md",
        "Source Code": "https://github.com/matheusfelipeog/froxy",
    },
    keywords=[
        'froxy', 
        'ip', 'hide ip', 'requests',
        'proxy', 'free proxy', 'proxy list', 
        'proxies', 'free proxies', 'proxies list'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
