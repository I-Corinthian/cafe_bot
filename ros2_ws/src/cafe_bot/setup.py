from setuptools import find_packages, setup

package_name = 'cafe_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name + '/launch', ['launch/launch_sim.launch.py','launch/turtle_launch.py','launch/nav_launch.py']),
        ('share/' + package_name + '/worlds', ['worlds/cafe.world','worlds/cafe1.world','worlds/cafe_new.world']),
        ('share/' + package_name + '/maps', ['maps/cafe_map.pgm','maps/cafe_map.yaml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='i_corinthian',
    maintainer_email='simonjoshua312@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
          'nav_goal_publisher = cafe_bot.nav_goal_publisher:main',
        ],
    },
)
