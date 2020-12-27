from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    README = f.read()


def requirements(filename):
    with open(filename, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                yield line


setup(
    name='NEMCore',
    version='0.1.6',
    author='weak_ptr',
    author_email='weak_ptr@outlook.com',
    description='NetEase Cloud Music API wrapper',
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=requirements('requirements/requirements.txt'),
    packages=find_packages(exclude=('tests', 'demo')),
    extras_require={
        'demo': requirements('requirements/demo.txt'),
        'lint': requirements('requirements/lint.txt'),
        'test': requirements('requirements/test.txt'),
        'docs': requirements('requirements/docs.txt'),
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
