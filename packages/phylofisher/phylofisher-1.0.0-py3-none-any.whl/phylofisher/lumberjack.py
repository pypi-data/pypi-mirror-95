#!/usr/bin/env python
import configparser
import glob
import os
import random
import shutil
import string
import tarfile
import textwrap
from collections import defaultdict
from datetime import date
from pathlib import Path

from Bio import SeqIO
import pandas as pd

from phylofisher import help_formatter, subset_tools
from phylofisher.utilities import build_database


def dataset_orgs():
    """"Collect all short names from dataset metadata table."""
    orgs = set()
    with open(metadata) as md:
        # skip header
        next(md)
        for line_ in md:
            sline = line_.split('\t')
            abbrev = sline[0].strip()
            orgs.add(abbrev)
    return orgs


def taxa_to_exclude():
    to_skip = set()
    with open(args.to_exclude, 'w') as infile:
        for line in infile:
            unique_id = line.strip().split(',')[0]
            to_skip.add(unique_id)

    return to_skip


def parse_input(input_metadata):
    """"Parse input metadata.
    input: input metadata csv
    return: dictionary with info about input metadata
    """
    orgs_to_exc = set()
    if args.to_exclude:
        orgs_to_exc = taxa_to_exclude()
    input_info = defaultdict(dict)
    for line in open(input_metadata):
        sline = line.split('\t')
        abbrev = sline[2].strip()
        if abbrev in orgs_to_exc:
            pass
        else:
            group = sline[3].strip()
            full_name = sline[6].strip()
            subtax = sline[4]
            data_type = sline[7]
            notes = sline[8].strip()
            input_info[abbrev]['tax'] = group
            input_info[abbrev]['full_name'] = full_name
            input_info[abbrev]['subtax'] = subtax
            input_info[abbrev]['data_type'] = data_type
            input_info[abbrev]['notes'] = notes
    return input_info


def collect_seqs(gene):
    """Collect all sequences for a given gene from fasta folder (fisher result)
    and store them in a dictionary.
    input: gene name
    return: dictionary of all seqs for a given gene
    """
    seq_dict = {}
    for record in SeqIO.parse(f'{fisher_dir}/{gene}.fas', 'fasta'):
        if record.name.count('_') == 3:
            abbrev, _, _, quality = record.name.split('_')
            qname = f'{abbrev}_{quality}'
            seq_dict[qname] = record
        else:
            seq_dict[record.name] = record
    return seq_dict


def id_generator(size=5, chars=string.digits):
    """"Generate random number with 5 digits."""
    return ''.join(random.choice(chars) for _ in range(size))


def paralog_name(abbrev, keys):
    """"Prepare paralog name (short name + 5 random digits).
    Recursive function.
    example: Homosap..12345
    input: short name of an organism, names of already existing paralogs
    for a given organism
    return: unique paralog name"""
    id_ = id_generator()
    pname = f'{abbrev}..p{id_}'
    if pname not in keys:
        return pname
    else:
        paralog_name(abbrev, keys)


def parse_table(table):
    """Collect information what has to be changed in
        the PhyloFisher dataset (for a given gene)
        according to information from
        parsed single gene tree.

     input: tsv table of one gene
     return: dictionaries of new orthologs and paralogs"""

    # gene name
    gene = table.split('/')[-1].split('_parsed')[0]
    # path to orthologs in the dataset folder
    orthologs_path = str(Path(dfo, f'orthologs/{gene}.fas'))
    # path to paralogs in the dataset folder
    paralogs_path = str(Path(dfo, f'paralogs/{gene}_paralogs.fas'))

    # parse orthologs for a given gene into a dictionary
    orthologs = SeqIO.to_dict(SeqIO.parse(orthologs_path, "fasta"))

    if os.path.isfile(paralogs_path):
        # parse paralogs a given gene into a dictionary (if they exist)
        paralogs = SeqIO.to_dict(SeqIO.parse(paralogs_path, "fasta"))
    else:
        # if paralogs doesnt exist, make an empty directory
        paralogs = {}

    # collect all candidate sequences for a given gen from the fisher.py result
    seq_dict = collect_seqs(gene)

    for line in open(table):
        # for orthologs from the dataset
        tree_name, tax, status = line.split('\t')
        status = status.strip()  # o,p,d (ortholog, paralog, delete)
        abbrev = tree_name.split('@')[-1]
        if tree_name.count('_') != 3 and '..' not in abbrev:
            record = seq_dict[abbrev]
            if status == 'd':
                # delete sequence from orthologs
                del orthologs[abbrev]
            elif status == 'p':
                # chance status from paralog to ortholog
                # prepare paralog name
                pname = paralog_name(abbrev, paralogs.keys())
                paralogs[pname] = record
                # delete sequence from orthologs
                del orthologs[abbrev]

    for line in open(table):
        # for new sequences
        tree_name, tax, status = line.split('\t')
        status = status.strip()
        abbrev = tree_name.split('@')[-1]
        if tree_name.count('_') == 3:
            quality = tree_name.split('_')[2]
            qname = f'{abbrev}_{quality}'
            record = seq_dict[qname]
            if status == 'o':
                # add to orthologs
                orthologs[abbrev] = record
            elif status == 'p':
                # add to paralogs
                pname = paralog_name(abbrev, paralogs.keys())
                paralogs[pname] = record

    for line in open(table):
        # for paralogs from the dataset
        tree_name, tax, status = line.split('\t')
        status = status.strip()
        name = tree_name.split('@')[-1]
        abbrev = name.split('.')[0]
        if '..' in name:
            record = paralogs[name]
            if status == 'o':
                # for cases when ortholog has not survived trimming
                if abbrev in orthologs:
                    # prepare paralog name
                    pname = paralog_name(abbrev, paralogs.keys())
                    # chance status from paralog to ortholog
                    paralogs[pname] = orthologs[abbrev]
                    # record in orthologs will be replaced
                    # with a new one in the next step
                # add sequence to orthologs 
                orthologs[abbrev] = record
                # delete sequence from paralogs
                del paralogs[name]
            elif status == 'd':
                # delete sequence
                del paralogs[name]

    return orthologs, paralogs


def add_to_meta(abbrev):
    """"Transfer input metadata for a given organism
    to dataset metadata.
    input:  short name of organism
    return: None
    """
    new_row = {'Unique ID': abbrev,
               'Long Name': input_info[abbrev]['full_name'],
               'Higher Taxonomy': input_info[abbrev]['tax'].replace('*', ''),
               'Lower Taxonomy': input_info[abbrev]['subtax'].replace('*', ''),
               'Data Type': input_info[abbrev]['data_type'],
               'Notes': input_info[abbrev]['notes']
               }

    taxa_comp, gene_count = subset_tools.completeness(args, str(Path(dfo, f'orthologs/')), genes=False)
    bin_matrix = subset_tools.completeness(args, str(Path(dfo, f'orthologs/')), genes=True)
    taxa_comp = taxa_comp.to_dict()

    df = pd.read_csv(metadata, delimiter='\t')
    df = df.set_index('Unique ID')

    comp_list = [taxa_comp[ind] if ind in taxa_comp else 0 for ind in df.index]
    df['Completeness'] = comp_list
    df['Completeness'] = df['Completeness'] * 100
    df['Completeness'] = df['Completeness'].round(2)

    # df = df.append(new_row, ignore_index=True)
    df = df.sort_values(by=['Higher Taxonomy', 'Lower Taxonomy', 'Unique ID'])
    df.to_csv('metadata.tsv', sep='\t', index=False)

    print(bin_matrix)
    print(df)


def new_database(table):
    """Make changes in the PhyloFisher dataset according to information from
     parsed single gene tree."""

    gene = table.split('/')[-1].split('_parsed')[0]
    # Orthologs for a given gene
    orthologs_path = str(Path(dfo, f'orthologs/{gene}.fas'))
    # Paralogs for a given gene
    paralogs_path = str(Path(dfo, f'paralogs/{gene}_paralogs.fas'))

    orthologs, paralogs = parse_table(table)

    with open(orthologs_path, 'w') as res:
        # make changes in orthologs
        for name, record in orthologs.items():
            if name not in meta_orgs:
                meta_orgs.add(name)
                add_to_meta(name)
            res.write(f'>{name}\n{record.seq}\n')

    with open(paralogs_path, 'w') as res:
        # make changes in paralogs
        for name, record in paralogs.items():
            if name.split('.')[0] not in meta_orgs:
                meta_orgs.add(name.split('.')[0])
                add_to_meta(name.split('.')[0])
            res.write(f'>{name}\n{record.seq}\n')


def backup():
    """
    Backs up database/orthologs/, database/paralogs/, and database/metadata.tsv before applying decisions
    :return: NONE
    """
    today_date = date.today().strftime("%b_%d_%Y")
    source_dir = f'{dfo}/backups/{today_date}'

    shutil.copytree(f'{dfo}/orthologs/', f'{source_dir}/orthologs')
    shutil.copytree(f'{dfo}/paralogs/', f'{source_dir}/paralogs')
    shutil.copy(f'{dfo}/metadata.tsv', f'{source_dir}/metadata.tsv')
    shutil.copy(f'{dfo}/tree_colors.csv', f'{source_dir}/tree_colors.csv')

    with tarfile.open(f'{source_dir}.tar.gz', "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    shutil.rmtree(source_dir)


def rebuild_db():
    """
    
    :return: 
    """
    try:
        shutil.rmtree(f'{dfo}/profiles')
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(f'{dfo}/datasetdb')
    except FileNotFoundError:
        pass
    
    cwd = os.getcwd()
    os.chdir(dfo)
    args.rename = None
    build_database.main(args, 4, True, 0.1)
    os.chdir(cwd)


def main():
    """
    Main function. Run new_database on all parsed trees (tsv files)
    :return:
    """
    for table in glob.glob(f'{args.input}/*_parsed.tsv'):
        new_database(table)

    rebuild_db()

    matrix = subset_tools.completeness(args, f'{dfo}/orthologs')
    matrix.to_csv(f'{dfo}/bin_matrix.tsv', sep='\t')
    print(matrix)

if __name__ == '__main__':
    desc = ''
    parser, optional, required = help_formatter.initialize_argparse(name='lumberjack.py',
                                                                    desc=desc,
                                                                    usage="lumberjack.py -i <in_dir>")

    required.add_argument('-fi', '--fisher_dir', type=str, metavar='<fisher_dir>', required=True,
                          help=textwrap.dedent("""\
                          Path to fisher output directory to use for dataset addition.
                          """))

    optional.add_argument('--to_exclude', type=str, metavar='to_exclude.txt',
                          help=textwrap.dedent("""\
                          Path to .txt file containing Unique IDs of taxa to exclude from dataset 
                          addition with one taxon per line.
                          Example:
                            Unique ID (taxon 1)
                            Unique ID (taxon 2)
                            """))

    in_help = 'Path to forest output directory to use for database addition.'
    args = help_formatter.get_args(parser, optional, required, out_dir=False, pre_suf=False, in_help=in_help)

    fisher_dir = args.fisher_dir

    config = configparser.ConfigParser()
    config.read('config.ini')
    dfo = str(Path(config['PATHS']['database_folder']).resolve())

    if not os.path.isdir(f'{dfo}/backups'):
        os.mkdir(f'{dfo}/backups')
    backup()

    input_metadata = os.path.abspath(config['PATHS']['input_file'])
    metadata = str(Path(dfo, 'metadata.tsv'))
    meta_orgs = dataset_orgs()
    input_info = parse_input(input_metadata)
    main()
