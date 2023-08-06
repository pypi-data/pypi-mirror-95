#!/usr/bin/env python
import os
import sys
import textwrap

import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as shc
from Bio import SeqIO, Phylo
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from ete3 import Tree, NodeStyle, TreeStyle, TextFace, CircleFace

from phylofisher import help_formatter


def distance_matrix2tree(Z, names):
    """Return tree representation for distance matrix"""
    n = Z.shape[0] + 1
    i2n = [0] * (2 * n - 1)
    t = Tree()
    for i, (idx1, idx2, dist, sample_count) in enumerate(Z):
        idx1, idx2 = int(idx1), int(idx2)
        # create Tree object for tips / leaves
        if idx1 < n:
            i2n[idx1] = Tree(name=names[idx1])
        if idx2 < n:
            i2n[idx2] = Tree(name=names[idx2])
        # create new node
        t = Tree()
        # normalise distance
        dist1 = dist - i2n[idx1].get_farthest_leaf()[1]
        dist2 = dist - i2n[idx2].get_farthest_leaf()[1]
        # add children
        t.add_child(i2n[idx1], dist=dist1)
        t.add_child(i2n[idx2], dist=dist2)
        # store
        i2n[n + i] = t
    return t


def aa_comp_calc():
    peptides = ['A', 'G', 'P', 'S', 'T', 'C', 'F', 'W', 'Y', 'H', 'R', 'K', 'M', 'I', 'L', 'V', 'N', 'D', 'E', 'Q']
    if not os.path.isdir(args.output):
        os.mkdir(args.output)
    with open(args.input, 'r') as infile, open(f'{args.output}/aa_comp.tsv', 'w') as outfile:
        outfile.write('Taxon\t' + '\t'.join(peptides) + '\n')

        # Reads in input file
        for record in SeqIO.parse(infile, format=args.in_format):
            outfile.write(f'{record.id}\t')
            analysed_seq = ProteinAnalysis(str(record.seq))
            count_dict = analysed_seq.count_amino_acids()
            length = len(str(record.seq).replace("-", "").replace("X", "").replace("*", ""))
            out_str = ''

            # Loops through peptides and checks to see if it is in count_dict
            for pep in peptides:
                if pep in count_dict.keys():
                    out_str += f'{float(count_dict[pep]) / length}\t'
                else:
                    out_str += '0\t'

            outfile.write(out_str.strip() + '\n')


def parse_tree_colors():
    color_dict = {}
    tree_color_dict = {}
    meta_dict = {}

    with open(tree_colors, 'r') as infile:
        infile.readline()
        for line in infile:
            s_line = line.strip().split('\t')
            tree_color_dict[s_line[0]] = s_line[1]

    with open(metadata, 'r') as infile:
        infile.readline()
        for line in infile:
            s_line = line.strip().split('\t')
            meta_dict[s_line[0]] = s_line[2:4]

    for k, v in meta_dict.items():
        if k in tree_color_dict.keys():
            color_dict[k] = tree_color_dict[k]
        elif v[0] in tree_color_dict.keys():
            color_dict[k] = tree_color_dict[v[0]]
        elif v[1] in tree_color_dict.keys():
            color_dict[k] = tree_color_dict[v[1]]
        else:
            sys.exit(f'{k} is not in the tree_color.tsv')

    return color_dict, tree_color_dict


def make_plot():
    color_dict, tree_color_dict = parse_tree_colors()
    df = pd.read_csv(f'{args.output}/aa_comp.tsv', sep="\t")
    df = df.set_index('Taxon')

    z = shc.linkage(df, method='ward')
    t = distance_matrix2tree(z, df.index.values)
    t.write(outfile=f'{args.output}/distance_matrix.tre')
    # t.unroot()

    # Basic tree style
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.mode = "c"
    ts.show_scale = False

    # Title formatting
    # title_face = TextFace("AA Composition Hierarchical Clustering", fsize=60)
    # ts.title.add_face(title_face, column=1)

    # Color Legend
    i, j = 0, 0
    for k, v in tree_color_dict.items():
        ts.legend.add_face(CircleFace(10, v), column=j)
        ts.legend.add_face(TextFace(k + ' '), column=j + 1)
        i += 1
        if i >= len(tree_color_dict.keys()) / 2:
            j = 2
    ts.legend_position = 4

    # Internal Node formatting
    nstyle_internal = NodeStyle()
    nstyle_internal["size"] = 0
    nstyle_internal["vt_line_width"] = 2
    nstyle_internal["hz_line_width"] = 2

    # Leaf formatting
    for n in t.traverse():
        if n.is_leaf():
            nstyle = NodeStyle()
            nstyle["bgcolor"] = color_dict[n.name]
            nstyle["vt_line_width"] = 1
            nstyle["hz_line_width"] = 1
            n.set_style(nstyle)
        else:
            n.set_style(nstyle_internal)

    # PDF rendering
    t.render(f'{args.output}/aa_comp_calculator.pdf', w=183, units="mm", tree_style=ts)


if __name__ == '__main__':
    description = 'Calculates amino acid composition of the supplied super matrix'
    parser, optional, required = help_formatter.initialize_argparse(name='aa_comp_calculator.py',
                                                                    desc=description,
                                                                    usage='aa_comp_calculator.py '
                                                                          '[OPTIONS] -i <matrix>')

    required.add_argument('-i', '--input', required=True, type=str, metavar='matrix',
                          help=textwrap.dedent("""\
                          Path to input matrix for analysis.
                          """))
    optional.add_argument('-if', '--in_format', metavar='<format>', type=str, default='fasta',
                          help=textwrap.dedent("""\
                          Format of input matrix.
                          Options: fasta, nexus, phylip (names truncated at 10 characters), 
                          Default: fasta
                          """))

    args = help_formatter.get_args(parser, optional, required, pre_suf=False, inp_dir=False)

    tree_colors = 'tree_colors.tsv'
    metadata = 'metadata.tsv'

    aa_comp_calc()
    make_plot()
