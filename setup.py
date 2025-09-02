from distutils.core import setup

setup(
    name='thorlabs_ccs',
    author='Martin Privat',
    version='0.2.20',
    packages=['thorlabs_ccs', 'thorlabs_pmd'],
    license='LGPL2.1',
    description='Control Thorlabs devices',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy",
        "pyUSB",
        "libusb-package",
        "python-usbtmc",
        "matplotlib"
    ]
)
