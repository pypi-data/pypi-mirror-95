import sys
import argparse
import tempfile
from lib.aggregate_all_epitopes import *

def define_parser():
    parser = argparse.ArgumentParser(
        "pvacfuse generate_aggregated_report",
        description="Generate an aggregated report from a pVACfuse .all_epitopes.tsv report file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "input_file",
        help="A pVACfuse .all_epitopes.tsv report file"
    )
    parser.add_argument(
        "output_file",
        help="The file path to write the aggregated report tsv to"
    )

    return parser

def main(args_input = sys.argv[1:]):
    parser = define_parser()
    args = parser.parse_args(args_input)

    tmp_fh = tempfile.NamedTemporaryFile()

    print("Creating Aggreggated Report")
    AggregateAllEpitopes(args.input_file, args.output_file, 'bedpe').execute()
    print("Completed")

if __name__ == '__main__':
    main()
