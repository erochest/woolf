#!/usr/bin/env python


"""This takes a classifier and an input document and marks the quotes
in it, based on the classifier."""

# TODO: Only show new quotation marks.


import argparse
from collections import deque
import pickle
import sys

import train_quotes
from fset_manager import Current


def load_classifier(filename):
    """Loads the classifier from pickled into `filename`."""
    with open(filename, 'rb') as fin:
        return pickle.load(fin)


# TODO: This interface should be changed. It should return whether or not the
# feature set represents a quotation.
def insert_quotes(classifier, fsets, sentence):
    """Identifies points in the input where quotes should be inserted."""
    for (features, span, _) in fsets:
        yield (features, span, classifier.classify(features))


def quote_output(classifier, manager, input_file, tagged_tokens, output_file):
    """\
    Classifies input sentences for quotes. This assumes that the classifier
    identifies points in the input where quotation marks should be inserted.

    In other words, we no longer use this.
    """

    quotes = []

    # before we could easily insert quotes. maybe not so now?
    for sentence in tagged_tokens:
        quotes += insert_quotes(
            classifier,
            manager.get_training_features(sentence),
            sentence
        )
    quotes.reverse()

    with open(input_file) as fin:
        data = fin.read()

    buf = deque()
    prev = None
    for i in quotes:
        if prev is None:
            slic = data[i:]
        else:
            slic = data[i:prev]

        buf.appendleft(slic)
        buf.appendleft("^")
        prev = i
    buf.appendleft(data[:prev])

    with open(output_file, 'w') as fout:
        fout.write(''.join(buf))


def parse_args(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-i', '--input', dest='input', action='store',
                        metavar='INPUT_FILE',
                        help='The input document to mark with quotes.')
    parser.add_argument('-c', '--classifier', dest='classifier',
                        action='store', metavar='PICKLE_FILE',
                        help='The classifier to use marking the quotes.')
    parser.add_argument('-o', '--output', dest='output', metavar='OUTPUT_FILE',
                        help='The file to write the output sentences to.')

    return parser.parse_args(argv)


def main():
    # parse arguments
    args = parse_args()
    # loads classifier
    classifier = load_classifier(args.classifier)
    # creates featureset manager based on the classifier
    manager = Current(train_quotes.is_quote, train_quotes.is_word)

    with open(args.output, 'w') as fout:
        with open(args.input) as fin:
            data = find.read()

        for sentence in manager.get_tagged_tokens(args.input):
            quotes = insert_quotes(
                classifier,
                manager.get_training_features(sentence),
                sentence
            )

            prev_quoted = False
            for (_, span, quoted) in quotes:
                if prev_quoted != quoted:
                    fout.write('^')
                    prev_quoted = quoted
                fout.write(data[start:end])


if __name__ == '__main__':
    main()
