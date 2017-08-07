from setuptools import setup, find_packages

setup(
    name='Lexos',
    version="4.0rc1",
    url='http://wheatoncollege.edu/lexomics/',
    license='MIT',
    author='WheatonCS/LexomicsResearch',
    author_email='',
    description='Python/Flask-based website for text analysis workflow. '
                'Previous (stable) release is live at: '
                'http://lexos.wheatoncollege.edu ',
    long_description="TODO",
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'flask',
        'numpy',
        'scikit-learn',
        'scipy',
        'pandas',
        'gensim',
        'beautifulsoup4',
        'lxml',
        'matplotlib',
        'chardet',
        'natsort',
        'plotly'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education :: Text Processing :: Utilities'
    ],
    entry_points='''
        [console_scripts]
        lexos=lexos.application:run
    '''
)
