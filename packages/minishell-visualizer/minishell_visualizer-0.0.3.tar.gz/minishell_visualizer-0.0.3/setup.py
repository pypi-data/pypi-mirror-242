from setuptools import setup, find_packages

setup(
    name='minishell_visualizer',
    version='0.0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'minishell_visualizer = minishell_visualizer.__main__:main'
        ]
    },
    install_requires=[
        # Add any dependencies your package needs
    ],
    # Other details like author, description, etc.
    author='Axel_chab',
    description='Simple minishell visualizer',
    # More details can be added
)