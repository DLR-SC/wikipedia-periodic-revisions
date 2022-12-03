from setuptools import setup

setup(
    name='wikipedia_tools',
    version='0.18.0',
    description='wikipedia_tools',
    #url='',
    author='Roxanne El Baff',
    author_email='roxanneelbaff@gmail.com',
    license='MIT',
    packages=['wikipedia_tools',
              'wikipedia_tools.analyzer',
              'wikipedia_tools.processor',
              'wikipedia_tools.scraper',
              'wikipedia_tools.utils'],
    install_requires=['pandas>=1.0.1',
                      'matplotlib>=3.2.1',
                      'pymediawiki==0.7.2',
                      'IPy>=1.01',
                      'seaborn>=0.11.2',
                      'textmining_utility>=0.2.0',
                      'tqdm==4.43.0',
                      'dataclasses==0.6',
                      'wikipedia_w_time @git+https://readonlytoken:FJ8a8jzPMtQ_jZQ9HFR1@gitlab.dlr.de/insightsnet/inisightsnet_code.git@main#subdirectory=insightsnet_wiki/wikipedia_w_time'
                      ],
    include_package_data=True,
    package_data={"../data": ["*"]},

)