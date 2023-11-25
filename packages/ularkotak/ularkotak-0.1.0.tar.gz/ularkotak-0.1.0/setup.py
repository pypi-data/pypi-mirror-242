from setuptools import setup, find_packages

setup(
    name='ularkotak',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
    ],
    author='Untara Eka Saputra',
    author_email='untara337@gmail.com',
    description='A simple game library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/codewithun/ularkotak.git',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
