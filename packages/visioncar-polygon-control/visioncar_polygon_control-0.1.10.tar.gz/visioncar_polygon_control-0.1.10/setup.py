import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='visioncar_polygon_control',
    author='VisionCar team',
    description='PySide6 application for controlling polygon elements',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': '.'},
    packages=setuptools.find_packages(where='.'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['PySide6==6.6.*', 'qt-material==2.*', 'requests==2.31.*', 'zeroconf', 'QtAwesome==1.2.*'],
    entry_points={
        'console_scripts': [
            'visioncar-polygon-control=visioncar_polygon_control:main.run'
        ],
    },
)
