"""compute sequence signatures for inputs"""

usage="""

   sourmash compute -k 21,31,51 *.fa *.fq

Create MinHash sketches at k-mer sizes of 21, 31 and 51, for
all FASTA and FASTQ files in the current directory, and save them in
signature files ending in '.sig'. You can rapidly compare these files
with `compare` and query them with `search`, among other operations;
see the full documentation at http://sourmash.rtfd.io/.

The key options for compute are:

 * `-k/--ksize <int>[, <int>]: k-mer size(s) to use, e.g. -k 21,31,51
 * `-n/--num <int>` or `--scaled <int>`: set size or resolution of sketches
 * `--track-abundance`: track abundances of hashes (default False)
 * `--dna or --protein`: nucleotide and/or protein signatures (default `--dna`)
 * `--merge <name>`: compute a merged signature across all inputs.
 * `--singleton`: compute individual signatures for each sequence.
 * `--name-from-first`: set name of signature from first sequence in file.
 * `-o/--output`: save all computed signatures to this file.

Please see -h for all of the options as well as more detailed help.

---
"""

from argparse import FileType

from sourmash.minhash import get_minhash_default_seed
from sourmash.cli.utils import add_construct_moltype_args
from sourmash.logging import notify


def ksize_parser(ksizes):
    # get list of k-mer sizes for which to compute sketches
    if ',' in ksizes:
        ksizes = ksizes.split(',')
        ksizes = list(map(int, ksizes))
    else:
        ksizes = [int(ksizes)]

    return ksizes


def subparser(subparsers):
    subparser = subparsers.add_parser('compute', description=__doc__, usage=usage)

    sketch_args = subparser.add_argument_group('Sketching options')
    sketch_args.add_argument(
        '-k', '--ksizes', default='21,31,51',
        type=ksize_parser,
        help='comma-separated list of k-mer sizes; default=%(default)s'
    )
    sketch_args.add_argument(
        '-n', '--num-hashes', type=int, default=500,
        help='number of hashes to use in each sketch; default=%(default)i'
    )
    sketch_args.add_argument(
        '--track-abundance', action='store_true',
        help='track k-mer abundances in the generated signature'
    )
    sketch_args.add_argument(
        '--scaled', type=float, default=0,
        help='choose number of hashes as 1 in FRACTION of input k-mers'
    )
    add_construct_moltype_args(sketch_args)
    sketch_args.add_argument(
        '--input-is-protein', action='store_true',
        help='Consume protein sequences - no translation needed.'
    )
    sketch_args.add_argument(
        '--seed', type=int, default=get_minhash_default_seed(),
        help='seed used by MurmurHash; default=%(default)i'
    )

    tenx_args = subparser.add_argument_group('10x options')
    tenx_args.add_argument(
        '--input-is-10x', action='store_true',
        help='input is 10x single cell output folder'
    )
    tenx_args.add_argument(
        '--count-valid-reads', default=0, type=int,
        help='a barcode is only considered a valid barcode read and its '
        'signature is written if number of umis are greater than '
        'count-valid-reads. It is used to weed out cell barcodes with few '
        'umis that might have been due to false rna enzyme reactions'
    )
    tenx_args.add_argument(
        '--write-barcode-meta-csv', type=str,
        help='for each of the unique barcodes, Write to a given path, number '
        'of reads and number of umis per barcode.'
    )
    tenx_args.add_argument(
        '-p', '--processes', default=2, type=int,
        help='number of processes to use for reading 10x bam file'
    )
    tenx_args.add_argument(
        '--save-fastas', default="", type=str,
        help='save merged fastas for all the unique barcodes to '
        '{CELL_BARCODE}.fasta in the absolute path given by this flag; by '
        'default, fastas are not saved'
    )
    tenx_args.add_argument(
        '--line-count', type=int, default=1500,
        help='line count for each bam shard',
    )
    tenx_args.add_argument(
        '--rename-10x-barcodes', metavar='FILE',
        help='Tab-separated file mapping 10x barcode name to new name, e.g. '
        'with channel or cell annotation label'
    )
    tenx_args.add_argument(
        '--barcodes-file', metavar='FILE',
        help='Barcodes file if the input is unfiltered 10x bam file'
    )

    file_args = subparser.add_argument_group('File handling options')
    file_args.add_argument(
        '-f', '--force', action='store_true',
        help='recompute signatures even if the file exists'
    )
    file_args.add_argument(
        '-o', '--output',
        help='output computed signatures to this file'
    )
    file_args.add_argument(
        '--outdir', help='output computed signatures to this directory'
    )
    file_args.add_argument(
        '--singleton', action='store_true',
        help='compute a signature for each sequence record individually'
    )
    file_args.add_argument(
        '--merge', '--name', type=str, default='', metavar="FILE",
        help='merge all input files into one signature file with the '
        'specified name'
    )
    file_args.add_argument(
        '--name-from-first', action='store_true',
        help='name the signature generated from each file after the first '
        'record in the file'
    )
    file_args.add_argument(
        '--randomize', action='store_true',
        help='shuffle the list of input filenames randomly'
    )

    subparser.add_argument(
        '-q', '--quiet', action='store_true', help='suppress non-error output'
    )
    subparser.add_argument(
        '--check-sequence', action='store_true',
        help='complain if input sequence is invalid'
    )
    subparser.add_argument(
        '--license', default='CC0', type=str,
        help='signature license. Currently only CC0 is supported.'
    )

    subparser.add_argument(
        'filenames', nargs='+', help='file(s) of sequences'
    )
    subparser._positionals.title = 'Required arguments'
    subparser._optionals.title = 'Miscellaneous options'


def main(args):
    from sourmash.command_compute import compute
    if args.input_is_10x:
        notify("** WARNING: 10x support is deprecated as of sourmash 3.5.x, and will")
        notify("**    be removed in sourmash 4.0; use kmermaid instead.")
        notify('')
    return compute(args)
