"""Main entry point for the cwl-pretty-graph tool."""
import argparse
import sys
import time

from cwl_graph_lib.logger import Logger
from cwl_graph_lib.cwl import load_workflow
from cwl_graph_lib.graph import CwlGraphHandler

def main():
    # setup logging
    start = time.time()

    # Set up root logger
    Logger.setup_root_logger()
    logger = Logger.get_logger('main')

    logger.info("*" * 60)
    logger.info("cwl-pretty-graph")
    logger.info("Create pretty graph images from a CWL workflow file")
    logger.info("Author: Kyle Hernandez <khernandez@bsd.uchicago.edu>")
    logger.info("Command line: {0}".format(" ".join(sys.argv[1:])))
    logger.info("*" * 60)
    
    # args
    args = get_args()

    # process
    logger.info("Loading workflow...")
    wfobj = load_workflow(args.workflow_file)

    # Initialize graph
    gv = CwlGraphHandler(args.output_prefix + '.gv', 
                         fmt=args.image_format, 
                         engine=args.engine)
    gv.process(wfobj)
 
def get_args():
    """Builds the command line arguments"""
    p = argparse.ArgumentParser(
        description="Create pretty graph images from a CWL workflow file"
    )

    p.add_argument('--engine', type=str, default='dot',
        help='The engine for clustering [dot]') 
    p.add_argument('--image_format', type=str, default='png',
        help='The format of the output image that is supported by graphviz [png]')
    p.add_argument('workflow_file', type=str,
        help='The input workflow file you want to create a graph for')
    p.add_argument('output_prefix', type=str,
        help='The path prefix for all output files')
    return p.parse_args()

if __name__ == '__main__':
    main()
