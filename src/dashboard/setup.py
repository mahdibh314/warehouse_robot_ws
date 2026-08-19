from setuptools import find_packages, setup

package_name = 'dashboard'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mahdi-ros',
    maintainer_email='mahdi2006.london@gmail.com',
    description='FastAPI web dashboard to monitor and control the warehouse robot',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
           'dashboard_node = dashboard.dashboard_node:main',
        ],
    },
)
