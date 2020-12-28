from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    README = f.read()

setup(
    name='NEMCore',
    version='0.1.6',
    author='weak_ptr',
    author_email='weak_ptr@outlook.com',
    description='NetEase Cloud Music API wrapper',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        "requests>=2.22.0",
        "pycryptodome>=3.9",
        "pycryptodomex>=3.9",
        "cachetools>=4.0",
        "filelock>=3.0"
    ],
    packages=find_packages(exclude=('tests',)),
    extras_require={
        'lint': [
            'pylint>=2.4',
            'autopep8>=1.4',
            'isort>=4.3',
        ],
        'test': [
            'pytest-cov>=2.7',
            'pytest-dotenv>=0.4.0',
            'pytest-mock>=1.11',
        ],
        'docs': [
            'mkdocs>=1.1.2',
            'mkdocs-material>=6.2.2',
        ],
    },
    keywords='NetEase Cloud Music API SDK',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3 :: Only',
        'Typing :: Typed'
    ],
    python_requires='>=3.6',
    url='https://github.com/nnnewb/nemcore',
)
