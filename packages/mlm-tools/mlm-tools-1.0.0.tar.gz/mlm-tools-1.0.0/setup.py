from setuptools import setup, find_packages

setup(
    name='mlm-tools',
    version='1.0.0',
    description='Good tools for using language models developed by zhwang.',
    long_description='',
    # The project's main homepage.
    url='https://zhwang4ai.github.io/',
    # Author details
    author='wangzihao',
    author_email='zhwang@stu.pku.edu.cn',
    # Choose your license
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(),
    py_modules=["zhwang4ai"],
    install_requires=[
        'openai'
        ]
)