#!/usr/bin/python

"""A clever way to run things in a terminal would be:
year=2016
for type in creativity anniversary temple legacy ; do
  ./generate_contracts.py --template template_${type}.tex --csv grants_${type}_${year}.csv
done
"""

import argparse
import csv
import logging
import os
import os.path
import shlex
import subprocess
import sys

def generate_contract(filename, template, grant, project, artist, amount):
    """inputs should be properly escaped for tex."""
    with open('parameters.tex', 'w') as pfile:
        params = ['\\renewcommand{\\grant}{%s}\n' % grant,
                  '\\renewcommand{\\project}{%s}\n' % project,
                  '\\renewcommand{\\artist}{%s}\n' % artist,
                  '\\renewcommand{\\amount}{%s}\n' % amount]
        pfile.writelines(params)

    with open(filename, 'w') as output:
        output.write(template)

    proc = subprocess.Popen(shlex.split('pdflatex %s' % filename))
    proc.communicate()
    if proc.returncode != 0:
        logging.error('Error running pdflatex')
        sys.exit(1)

    os.unlink(filename)
    os.unlink(filename.replace('.tex', '.log'))
    os.unlink(filename.replace('.tex', '.aux'))
    os.unlink(filename.replace('.tex', '.out'))
    pdfname = filename.replace('.tex', '.pdf')
    os.rename(pdfname, os.path.join('contracts', pdfname))
    os.unlink('parameters.tex')

def generate_from_csv(filename, template):
    """filename is the csv file, template is pre-read string of latex"""
    with open(filename, 'r') as input_file:
        grant_info = csv.reader(input_file)
        for row in grant_info:
            filename = row[1].replace(' ', '_')
            filename = filename.lower()
            filename += '.tex'
            generate_contract(filename, template, row[2], row[1], row[0],
                              row[3].replace('$','\$').replace(',',''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates art grant contracts')
    parser.add_argument('--template', type=str, help='.tex template file')
    parser.add_argument('--csv', type=str, help='csv file defining grants to output')

    args = parser.parse_args()
    if not args.template:
        logging.error('need to specify a template file')
        parser.print_usage()
        sys.exit(1)
    if not args.csv:
        logging.error('need to specify a csv file')
        parser.print_usage()
        sys.exit(1)
    if not os.path.isfile(args.template):
        logging.error('template file not found')
        sys.exit(1)
    if not os.path.isfile(args.csv):
        logging.error('csv file not found')
        sys.exit(1)

    template_filename = sys.argv[1]
    template = ''
    with open(args.template, 'r') as template_file:
        template = template_file.read()

    if not os.path.isdir('./contracts'):
        os.mkdir('./contracts')

    generate_from_csv(args.csv, template)
