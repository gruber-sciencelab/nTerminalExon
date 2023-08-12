##############################################################################
#
#   #QC plots
#
#   AUTHOR: Miguel_Barquin
#   AFFILIATION: Konstanz_University
#   CREATED: 12-05-2022
#   LICENSE: Apache_2.0
#
###############################################################################

# imports
import pandas as pd
import matplotlib.pyplot as plt
import yaml
import os
import time
import logging
import logging.handlers
from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np


def parse_arguments():
    """Parser of the command-line arguments."""
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-v",
        "--verbosity",
        dest="verbosity",
        choices=("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"),
        default="ERROR",
        help="Verbosity/Log level. Defaults to ERROR",
    )
    parser.add_argument(
        "-l", "--logfile", dest="logfile", help="Store log to this file."
    )
    parser.add_argument(
        "--mapping-quality-scores-rnaseqc",
        dest="mapping_quality_table_rnaseqc",
        required=True,
        help="Merged RNA-SeQC results per sample in a TSV format.",
    )
    parser.add_argument(
        "--mapping-quality-scores-star",
        dest="mapping_quality_table_star",
        required=True,
        help="Merged STAR results per sample in a TSV format.",
    )
    parser.add_argument(
        "--TIN-scores",
        dest="TIN",
        required=True,
        help="Median TIN scores per sample in a TSV format.",
    )
    parser.add_argument(
        "--design-table-in",
        dest="input",
        required=True,
        help="Original design table in a TSV format.",
    )
    parser.add_argument(
        "--qc-plot-out",
        dest="pdf_output",
        required=True,
        help="QC plots.",
    )
    parser.add_argument(
        "--min-median-TIN-cutoff",
        dest="TIN_cutoff",
        required=True,
        help="Minimal value for the median TIN score per sample.",
    )
    parser.add_argument(
        "--min-mapping-rate",
        dest="rnaseqc_min_mapping_rate",
        required=True,
        help="RNA-SeQC: minimal value for the Mapping Rate.",
    )
    parser.add_argument(
        "--min-unique-rate-of-mapped",
        dest="rnaseqc_min_unique_rate_of_mapped",
        required=True,
        help="RNA-SeQC: minimal value for the Unique Rate of Mapped.",
    )
    parser.add_argument(
        "--min-high-quality-rate",
        dest="rnaseqc_min_high_quality_rate",
        required=True,
        help="RNA-SeQC: minimal value for the High Quality Rate.",
    )
    parser.add_argument(
        "--max-intergenic-rate",
        dest="rnaseqc_max_intergenic_rate",
        required=True,
        help="RNA-SeQC: maximal value for the Intergenic Rate.",
    )
    parser.add_argument(
        "--max-rRNA-rate",
        dest="rnaseqc_max_rRNA_rate",
        required=True,
        help="RNA-SeQC: maximal value for the rRNA Rate.",
    )
    return parser

##############################################################################

def main():
    """Main body of the script."""

    samples_to_remove = []

    # read the original design table
    design_table_in = pd.read_csv(options.input, sep="\t", index_col=0)

    # quality filtering based on TIN score calculation
    TIN = pd.read_csv(options.TIN, sep="\t", header=None)
    new_header = ("Sample","TIN_value")
    TIN.columns = new_header
    TIN['TIN_value'] = TIN['TIN_value'].astype('float')

    # quality filtering based on the mapping scores (RNA-SeQC)
    rnaseqc_table = pd.read_csv(options.mapping_quality_table_rnaseqc, sep="\t", header=None)
    rnaseqc_transposed = rnaseqc_table.T
    new_header_rnaseqc = rnaseqc_transposed.iloc[0] #grab the first row for the header
    rnaseqc_transposed = rnaseqc_transposed[1:] #take the data less the header row
    rnaseqc_transposed.columns = new_header_rnaseqc
    
    # select the value we want to check
    rnaseqc_transposed['High Quality Rate'] = rnaseqc_transposed['High Quality Rate'].astype('float')
    rnaseqc_transposed['Intergenic Rate'] = rnaseqc_transposed['Intergenic Rate'].astype('float')
    rnaseqc_transposed['rRNA Rate'] = rnaseqc_transposed['rRNA Rate'].astype('float')

    # quality filtering based on the mapping scores (STAR)
    star_table = pd.read_csv(options.mapping_quality_table_star, sep="\t", header=None)
    star_transposed = star_table.T
    new_header_star = star_transposed.iloc[0] #grab the first row for the header
    star_transposed = star_transposed[1:] #take the data less the header row
    star_transposed.columns = new_header_star
    
    # select the value we want to check
    star_transposed['Mapping Rate'] = star_transposed['Mapping Rate'].astype('float')
    star_transposed['Unique Rate of Mapped'] = star_transposed['Unique Rate of Mapped'].astype('float')

    # RNA-SeQC quality filtering
    plt.figure(figsize=(10 + 0.2 * (len(rnaseqc_transposed.index)), 10 + 0.1 * (len(rnaseqc_transposed.index))))
    
    plt.subplot(2,3,1)
    plot_tin = plt.scatter(x='Sample', y='TIN_value', data=TIN)
    plt.ylim(bottom=0)
    plt.xticks(rotation = 90, fontsize=(0.01 * (len(rnaseqc_transposed.index))))
    plt.axhline(y=float(options.TIN_cutoff), color='r', linestyle='-')
    plt.title("TIN value", fontsize=(0.1 * (len(rnaseqc_transposed.index))))
    plt.axhspan(float(options.TIN_cutoff), 100, facecolor='palegreen', alpha=0.5)
    plt.axhspan(float(options.TIN_cutoff), 0, facecolor='lightcoral', alpha=0.5)

    plt.subplot(2,3,2)
    plot_mapping_rate = plt.scatter(x='Sample', y='Mapping Rate', data=star_transposed)
    plt.ylim(bottom=0)
    plt.xticks(rotation = 90, fontsize=(0.01 * (len(rnaseqc_transposed.index))))
    plt.axhline(y=float(options.rnaseqc_min_mapping_rate), color='r', linestyle='-')
    plt.title("Mapping Rate", fontsize=(0.1 * (len(rnaseqc_transposed.index))))
    plt.axhspan(float(options.rnaseqc_min_mapping_rate), 1, facecolor='palegreen', alpha=0.5)
    plt.axhspan(float(options.rnaseqc_min_mapping_rate), 0, facecolor='lightcoral', alpha=0.5)

    plt.subplot(2,3,3)
    plot_unique_rate_mapped = plt.scatter(x='Sample', y='Unique Rate of Mapped', data=star_transposed)
    plt.ylim(bottom=0)
    plt.xticks(rotation = 90, fontsize=(0.01 * (len(rnaseqc_transposed.index))))
    plt.axhline(y=float(options.rnaseqc_min_unique_rate_of_mapped), color='r', linestyle='-')
    plt.title("Unique Rate of Mapped Reads", fontsize=(0.1 * (len(rnaseqc_transposed.index))))
    plt.axhspan(float(options.rnaseqc_min_unique_rate_of_mapped), 1, facecolor='palegreen', alpha=0.5)
    plt.axhspan(float(options.rnaseqc_min_unique_rate_of_mapped), 0, facecolor='lightcoral', alpha=0.5)

    plt.subplot(2,3,4)
    plot_high_quality_rate = plt.scatter(x='Sample', y='High Quality Rate', data=rnaseqc_transposed)
    plt.ylim(bottom=0)
    plt.xticks(rotation = 90, fontsize=(0.01 * (len(rnaseqc_transposed.index))))
    plt.axhline(y=float(options.rnaseqc_min_high_quality_rate), color='r', linestyle='-')
    plt.title("High Quality Rate", fontsize=(0.1 * (len(rnaseqc_transposed.index))))
    plt.axhspan(float(options.rnaseqc_min_high_quality_rate), 1, facecolor='palegreen', alpha=0.5)
    plt.axhspan(float(options.rnaseqc_min_high_quality_rate), 0, facecolor='lightcoral', alpha=0.5)


    plt.subplot(2,3,5)
    plot_intergenic_rate = plt.scatter(x='Sample', y='Intergenic Rate', data=rnaseqc_transposed)
    plt.ylim(bottom=0)
    plt.xticks(rotation = 90, fontsize=(0.01 * (len(rnaseqc_transposed.index))))
    plt.axhline(y=float(options.rnaseqc_max_intergenic_rate), color='r', linestyle='-')
    plt.title("Intergenic Rate", fontsize=(0.1 * (len(rnaseqc_transposed.index))))
    plt.axhspan(0, float(options.rnaseqc_max_intergenic_rate), facecolor='palegreen', alpha=0.5)
    plt.axhspan(float(options.rnaseqc_max_intergenic_rate), 1, facecolor='lightcoral', alpha=0.5)


    plt.subplot(2,3,6)
    plot_rrna_rate = plt.scatter(x='Sample', y='rRNA Rate', data=rnaseqc_transposed)
    plt.ylim(bottom=0)
    plt.xticks(rotation = 90, fontsize=(0.01 * (len(rnaseqc_transposed.index))))
    plt.axhline(y=float(options.rnaseqc_max_rRNA_rate), color='r', linestyle='-')
    plt.title("rRNA Rate", fontsize=(0.1 * (len(rnaseqc_transposed.index))))
    plt.axhspan(0, float(options.rnaseqc_max_rRNA_rate), facecolor='palegreen', alpha=0.5)
    plt.axhspan(float(options.rnaseqc_max_rRNA_rate), 1, facecolor='lightcoral', alpha=0.5)


    plt.tight_layout()
    plt.savefig(options.pdf_output)

##############################################################################

if __name__ == "__main__":

    try:
        # parse the command-line arguments
        options = parse_arguments().parse_args()

        # set up logging during the execution
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s - %(message)s",
            datefmt="%d-%b-%Y %H:%M:%S",
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger = logging.getLogger("logger")
        logger.setLevel(logging.getLevelName(options.verbosity))
        logger.addHandler(console_handler)
        if options.logfile is not None:
            logfile_handler = logging.handlers.RotatingFileHandler(
                options.logfile, maxBytes=50000, backupCount=2
            )
            logfile_handler.setFormatter(formatter)
            logger.addHandler(logfile_handler)

        # execute the body of the script
        start_time = time.time()
        logger.info("Starting script")
        main()
        seconds = time.time() - start_time

        # log the execution time
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        logger.info(
            "Successfully finished in {hours}h:{minutes}m:{seconds}s",
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds) if seconds > 1.0 else 1,
        )
    # log the exception in case it happens
    except Exception as e:
        logger.exception(str(e))
        raise e