from setuptools import find_packages, setup

package_name = "message_logger"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jlotvone19",
    maintainer_email="jere.lotvonen@gmail.com",
    description="Logger for sensor message topics",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "listener = message_logger.logger:main",
        ],
    },
)
