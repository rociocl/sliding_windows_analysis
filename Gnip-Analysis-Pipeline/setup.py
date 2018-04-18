from setuptools import setup, find_packages

setup(name='gnip_analysis_pipeline',
        scripts=['tweet_enricher.py', 
            'tweet_time_series_builder.py', 
            ],
        version='1.1',
        license='MIT',
        author='Jeff Kolb',
        author_email='jeffakolb@gmail.com',
        description='A processing pipeline for enriching and aggregating Tweet data from Twitter APIs',
        url='https://github.com/tw-ddis/Gnip-Analysis-Pipeline',
        )
