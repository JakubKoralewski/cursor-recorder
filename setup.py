from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='cursor-recorder',
    version='0.1',
    description='Records cursor data',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jakub Koralewski',
    url='https://github.com/JakubKoralewski/cursor-recorder',
    packages=['cursor-recorder-for-afterfx'],  #same as name
    install_requires=['PyAutoGUI', 'keyboard'], #external packages as dependencies
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL-2.0)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3, <4',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/JakubKoralewski/cursor-recorder/issues',
        'Source': 'https://github.com/JakubKoralewski/cursor-recorder',
    },
)