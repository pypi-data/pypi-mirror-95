import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding='utf-8')

requirements = [
    'requests==2.25.1',
    'requests-toolbelt==0.9.1',
    'PySocks==1.7.1',
    'pydantic==1.7.3'
]

setup(
    name='radiojavanapi',
    version='0.1.1',
    author='xHossein',
    license='MIT',
    url='https://github.com/xHossein/radiojavanapi',
    install_requires=requirements,
    keywords='radiojavan private api',
    description='Fast and effective RadioJavan Private API',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)