from setuptools import setup

setup(
    name = "cwl_pretty_graph",
    author = "Kyle Hernandez",
    author_email = "khernandez@bsd.uchicago.edu",
    version = 0.1,
    description = "Prettier plotting of CWL workflows",
    url = "https://github.com/kmhernan/cwl-pretty-graph",
    license = "Apache 2.0",
    packages = ["cwl_graph_lib", "cwl_graph_cli"],
    package_dir = {"cwl_graph_lib": "src/cwl_graph_lib", "cwl_graph_cli": "src/cwl_graph_cli"},
    install_requires = [
        "cwltool==1.0.20170928192020",
        "graphviz==0.8"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
    ],
    entry_points= {
        'console_scripts': [
            'cwl-pretty-graph = cwl_graph_cli.__main__:main'
        ]
    },
)
