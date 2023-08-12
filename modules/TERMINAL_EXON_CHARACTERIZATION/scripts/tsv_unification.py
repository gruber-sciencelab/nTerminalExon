"""
##############################################################################
#
#   Filter design table based on the quality of RNA-Seq samples.
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   AFFILIATION: Swiss_Institute_of_Bioinformatics
#   CONTACT: maciej.bak@unibas.ch
#   CREATED: 02-05-2020
#   LICENSE: Apache_2.0
#
##############################################################################
"""

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
from pathlib import Path


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
        "--forward-tsv",
        dest="forward_tsv",
        required=True,
        help="Merged RNA-SeQC results per sample in a TSV format.",
    )
    parser.add_argument(
        "--reverse-tsv",
        dest="reverse_tsv",
        required=True,
        help="Merged STAR results per sample in a TSV format.",
    )
    parser.add_argument(
        "--final-tsv",
        dest="final_tsv",
        required=True,
        help="Median TIN scores per sample in a TSV format.",
    )
    return parser


##############################################################################



def main():
    """Main body of the script."""

    # Checking if the forward file has been created
    path_to_file_forward = os.path.join(options.forward_tsv,"classified_as_terminal_with_probabilities.tsv")
    path_forward = Path(path_to_file_forward)

    if path_forward.is_file():
        FORWARD = pd.read_csv(path_to_file_forward, sep="\t")
    else:
        FORWARD = pd.DataFrame(columns=['region'])
    
    # Checking if the reverse file has been created
    path_to_file_reverse = os.path.join(options.reverse_tsv,"classified_as_terminal_with_probabilities.tsv")
    path_reverse = Path(path_to_file_reverse)

    if path_reverse.is_file():
        REVERSE = pd.read_csv(path_to_file_reverse, sep="\t")
    else:
        REVERSE = pd.DataFrame(columns=['region'])
    
    # getting unique events for each file
    forward_unique = FORWARD[~FORWARD.region.isin(REVERSE.region)]
    reverse_unique = REVERSE[~REVERSE.region.isin(FORWARD.region)]

    # getting common events for each file
    forward_common = FORWARD[FORWARD.region.isin(REVERSE.region)]
    reverse_common = REVERSE[REVERSE.region.isin(FORWARD.region)]

    # selecting higher terminal_probability events for common events
    new_df = []

    for index, rowf in forward_common.iterrows():
        for index, rowr in reverse_common.iterrows():
            if (rowr['region'] == rowf['region']) and rowr['terminal_probability'] >= rowf['terminal_probability']:
                new_df.append(rowr)
            elif (rowr['region'] == rowf['region']) and rowr['terminal_probability'] < rowf['terminal_probability']:
                new_df.append(rowf)
            
    forward_reverse_common = pd.DataFrame(new_df)

    final_tsv = [forward_unique, reverse_unique, forward_reverse_common]
    result = pd.concat((final_tsv),ignore_index=True)

    result.to_csv((options.final_tsv), sep="\t")

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
