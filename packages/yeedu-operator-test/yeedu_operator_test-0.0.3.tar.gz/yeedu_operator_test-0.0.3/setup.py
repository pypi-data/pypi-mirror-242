from setuptools import setup, find_packages

setup(
    name='yeedu_operator_test',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'apache-airflow>=2.7.3',
        # Add any other dependencies here
    ],
    project_urls={
        'GitHub': 'https://github.com/rohith-sagar/AirflowYeeduOperator.git',
        'GitHub Issues': 'https://github.com/rohith-sagar/AirflowYeeduOperator.git/issues',
        'GitHub Statistics': 'https://github.com/rohith-sagar/AirflowYeeduOperator.git/graphs/contributors',
        # Add more URLs as needed
    },
)

