from setuptools import setup

setup(
    name='wikipedia_tools',
    version='1.1.0',
    description='wikipedia_tools',
    #url='',
    author='Roxanne El Baff',
    author_email='roxanneelbaff@gmail.com',
    license='MIT',
    packages=['wikipedia_tools',
              'wikipedia_tools.analyzer',
              'wikipedia_tools.processor',
              'wikipedia_tools.scraper',
              'wikipedia_tools.utils',
              'wikipedia_tools.base'],
    install_requires=['pandas>=1.0.1',
                      'matplotlib>=3.2.1',
                      'pymediawiki==0.7.2',
                      'IPy>=1.01',
                      'seaborn>=0.11.2',
                      'nlpaf',
                      'tqdm==4.43.0',
                      'dataclasses==0.6',
                      'beautifulsoup4',
                      'requests>=2.0.0,<3.0.0'
                      ],
    include_package_data=True,
    package_data={"../data": ["*"]},

)