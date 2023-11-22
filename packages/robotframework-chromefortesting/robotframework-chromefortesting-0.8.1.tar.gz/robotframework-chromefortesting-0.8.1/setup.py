from setuptools import setup, find_packages

setup(
    name='robotframework-chromefortesting',
    version='0.8.1',
    packages=find_packages(),
    package_data={'robotframework-chromefortesting': ['ChromeForTesting.py']},
    install_requires=[
        "requests",
        "robotframework"
    ],
    url='https://github.com/extraorange/robotframework-chromefortesting',
    author='extraorange',
    author_email='extraorangeio@pm.me',
    description='The only extension for seamless setup of Chrome for Testing (CfT) in and within Robot Framework.',
    license='GNU General Public License v3.0'
)