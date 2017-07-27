from setuptools import setup, find_packages

setup(name="Lexos",
      version="4.0rc1",
      description="Python/Flask-based website for text analysis workflow.",
      long_description="""TODO""",
      author="WheatonCS/LexomicsResearch",
      url="http://wheatoncollege.edu/lexomics/introduction-lexomics/",
      download_url="TODO",
      license="MIT",
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
      ],
      packages=find_packages('lexos')
      )
