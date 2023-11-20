from setuptools import setup, find_packages

setup(
    name='CharTurn',
    version='0.1',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    description='A turn-based combat system for RPGs.',
    packages=find_packages(),
    install_requires=['pyglet'],
    url='https://github.com/primal-coder/CharTurn',
    license='MIT',
    keywords=['turn-based', 'combat', 'RPG'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)