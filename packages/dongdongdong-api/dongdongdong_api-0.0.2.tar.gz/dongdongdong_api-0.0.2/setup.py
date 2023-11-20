from setuptools import setup, find_packages

setup(
    name                = 'dongdongdong_api',
    version             = '0.0.2',
    description         = 'Process signin and signup',
    author              = 'dongjae',
    author_email        = 'sdhsdj6450@gmail.com',
    install_requires    =  ["bcrypt", "python-dotenv", "PyJWT"],
    packages            = find_packages(exclude = []),
    url                 = 'https://github.com/dongdongjae/user_package',
    python_requires     = '>=3',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)