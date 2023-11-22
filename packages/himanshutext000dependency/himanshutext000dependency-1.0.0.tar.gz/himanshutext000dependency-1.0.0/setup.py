from setuptools import setup, find_packages

setup(
    name='himanshutext000dependency',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'mycollect-collect-data = mycollect.collect_data:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author='Your Name',
    author_email='your@email.com',
    description='A package for collecting and sending system data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mycollect',
)
