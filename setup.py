from distutils.core import setup

setup(
    name='thorlabs_ccs',
    author='Martin Privat',
    version='0.1.0',
    packages=['thorlabs_ccs'],
    license='LGPL2.1',
    description='Control Thorlabs CCS spectrometer',
    long_description=open('README.md').read(),
    install_requires=[
        "pyUSB",
        "libusb-package",
        "matplotlib"
    ]
)
