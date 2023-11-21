from setuptools import setup, find_packages

setup(
    name='DeepChat-AI',
    version='1.0.1',
    packages=find_packages(),
    description='MLChatbotAI is a Python package for building, training, and deploying machine learning-based chatbots.',
    long_description_content_type='text/markdown',
    author='Shibam Das',
    author_email='shibomdas121@gmail.com',
    license='MIT',
    url='https://github.com/ShibamDas007/python-DeepChat_AI',
    install_requires=[
        'numpy>=1.26.1',
        'tensorflow>=2.14.0',
        'keras>=2.14.0',
        'pyttsx3>=2.90',
        'nltk>=3.8.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
