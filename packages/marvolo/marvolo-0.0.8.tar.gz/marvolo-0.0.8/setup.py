from setuptools import setup

setup(
    name='marvolo',
    version='v0.0.8',
    description='Some useful tools about CV develeped by Marvolo',
    # py_modules=['marvolo'],
    platforms=['all'],
    author='Marvolo',
    author_email='18377221@buaa.edu.cn',
    python_requires='>=3.6',
    url='',
    install_requires=['opencv-python','imageio', 'colorlog'],
    license='MIT',
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
