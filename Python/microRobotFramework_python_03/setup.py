#!/usr/bin/env python3
"""
setup.py for microRobotFramework_03 Python package
"""

from setuptools import setup, find_packages
import os

# Read README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Python version of microRobotFramework Version 03 with multi-threading support"

# Read requirements file
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['pyserial>=3.5']

setup(
    name='microRobotFramework-03',
    version='3.0.0',
    author='JD-edu',
    author_email='',
    description='Python version of microRobotFramework Version 03 with multi-threading support',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/JD-edu/microRobotFramework',
    packages=find_packages(),
    py_modules=['microRobotFramework_03'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.7',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
        'examples': [
            'keyboard>=1.13.0',  # For advanced keyboard control examples
        ],
    },
    entry_points={
        'console_scripts': [
            'mrf-example-03=mrf_example_03:main',
            'mrf-threading=mrf_example_03:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt', '*.rst'],
    },
    keywords=[
        'robot',
        'robotics',
        'serial',
        'communication',
        'imu',
        'encoder',
        'sensor',
        'microcontroller',
        'arduino',
        '2-wheel robot',
        'autonomous robot',
        'multi-threading',
        'concurrent',
        'real-time',
        'motor control',
        'threading',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/JD-edu/microRobotFramework/issues',
        'Source': 'https://github.com/JD-edu/microRobotFramework',
        'Documentation': 'https://github.com/JD-edu/microRobotFramework/blob/main/README.md',
    },
)
