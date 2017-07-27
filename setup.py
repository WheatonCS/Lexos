from setuptools import setup, find_packages

setup(
    name="Lexos",
    version="4.0rc1",
    description="Python/Flask-based website for text analysis workflow.",
    long_description="""TODO""",
    author="WheatonCS/LexomicsResearch",
    url="http://wheatoncollege.edu/lexomics/introduction-lexomics/",
    download_url="TODO",
    license="MIT",
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lexos = lexos.application:run'
        ]
    },
    install_requires=[
        'flask',
        'numpy',
        'scikit-learn',
        'scipy',
        'beautifulsoup4',
        'lxml',
        'matplotlib',
        'chardet',
        'natsort',
        'plotly',
        'gensim'
    ]
)
