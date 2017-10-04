# cwl-pretty-graph
Creates simple graphviz plots from CWL workflows

## Requirements

_Installation with pip will automatically handle dependencies_

* Python 2
* `graphviz==0.8`
* `cwltool==1.0.20170928192020`

## Installation

1. clone the repository
2. `pip install /path/to/repo`

**Only Python 2 supported due to cwltool dependency**

## Usage

```
$ cwl-pretty-graph -h
[INFO] [22:29:30] [cwl_graph_lib.main] - ************************************************************
[INFO] [22:29:30] [cwl_graph_lib.main] - cwl-pretty-graph
[INFO] [22:29:30] [cwl_graph_lib.main] - Create pretty graph images from a CWL workflow file
[INFO] [22:29:30] [cwl_graph_lib.main] - Author: Kyle Hernandez <khernandez@bsd.uchicago.edu>
[INFO] [22:29:30] [cwl_graph_lib.main] - Command line: -h
[INFO] [22:29:30] [cwl_graph_lib.main] - ************************************************************
usage: cwl-pretty-graph [-h] [--image_format IMAGE_FORMAT]
                        workflow_file output_prefix

Create pretty graph images from a CWL workflow file

positional arguments:
  workflow_file         The input workflow file you want to create a graph for
  output_prefix         The path prefix for all output files

optional arguments:
  -h, --help            show this help message and exit
  --image_format IMAGE_FORMAT
                        The format of the output image that is supported by
                        graphviz [png]
```

This will create two output files: `<output_prefix>.gv` and `<output_prefix>.gv.<filetype>`.
