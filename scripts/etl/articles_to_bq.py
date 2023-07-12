import argparse
import logging
import csv
import io


import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


def read_csv_file(file):
    with beam.io.filesystems.FileSystems.open(file) as gcs_file:
        reader = csv.reader(io.TextIOWrapper(gcs_file))

        # Ignore headers
        next(reader)
        for row in reader:
            yield row


def run(argv=None):
    """The main function which creates the pipeline and runs it."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        required=False,
        help='Input file to read. This can be a local file or '
        'a file in a Google Storage Bucket.',
        default='articles_arxiv-202307101305.csv')
    parser.add_argument('--output',
                        dest='output',
                        required=False,
                        help='Output title',
                        default='test')

    known_args, pipeline_args = parser.parse_known_args(argv)


    p = beam.Pipeline(options=PipelineOptions(pipeline_args))
    beam.io.WriteToText
    (p
         | 'Load url' >> beam.Create([known_args.input])
         | 'Read csv' >> beam.FlatMap(read_csv_file)
         | 'String to text file' >> beam.io.WriteToText(known_args.output)
    )
    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
