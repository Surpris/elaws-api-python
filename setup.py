from setuptools import setup, find_packages

setup(
    name='elaws-api-python',
    version='0.0.1',
    description='Python wrapper for eLaws APIs of e-Gov',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Surpris/elaws-api-python',
    author='Surpris',
    author_email='take90-it09-easy27@outlook.jp',
    license='MIT',
    packages=find_packages(),
    package_data={
        'elaws_api_python': ['schema/*.xsd'],
    },
    include_package_data=True,
    install_requires=[
        'requests',
        'xmlschema'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)