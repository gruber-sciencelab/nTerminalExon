"""
##############################################################################
#
#   #STAR data
#
#   AUTHOR: Miguel_Barquin
#   AFFILIATION: Konstanz_University
#   CREATED: 10-08-2022
#   LICENSE: Apache_2.0
#
###############################################################################
"""
# imports

import os
import time
import logging
import logging.handlers
from argparse import ArgumentParser, RawTextHelpFormatter
import pandas as pd

def parse_arguments():
    '''Parser of the command-line arguments.'''
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("-v",
                        "--verbosity",
                        dest="verbosity",
                        choices=('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'),
                        default='ERROR',
                        help="Verbosity/Log level. Defaults to ERROR")
    parser.add_argument("-l",
                        "--logfile",
                        dest="logfile",
                        help="Store log to this file.")
    parser.add_argument("--samples-names",
                        dest="samples",
                        required=True,
                        nargs="+",
                        help="Name of samples.")
    parser.add_argument("--output-tsv",
                        dest="TSV",
                        required=True,
                        help="TSV file with STAR information.")
    return parser

##############################################################################

def main():
    '''Main body of the script.'''

    df_list = []
    for bam_path in options.samples:
        head_tail = os.path.split(bam_path)
        path = head_tail[0]
        sample = path.split("/")[-1]
        path = os.path.join(path,sample + '.Log.final.out')
        temp = pd.read_csv(path, sep="\t", index_col=0, header=None,
            na_values=['nan'], keep_default_na=False)
        temp.reset_index(drop=True, inplace=True)
        temp = temp.set_index([pd.Index(['Started job on',
        'Started mapping on', 
        'Finished on', 
        'Mapping speed, Million of reads per hour', 
        'Number of input reads', 
        'Average input read length', 
        'UNIQUE READS:', 
        'Uniquely mapped reads number', 
        'Uniquely mapped reads %', 
        'Average mapped length', 
        'Number of splices: Total', 
        'Number of splices: Annotated (sjdb)', 
        'Number of splices: GT/AG', 
        'Number of splices: GC/AG', 
        'Number of splices: AT/AC', 
        'Number of splices: Non-canonical', 
        'Mismatch rate per base, %', 
        'Deletion rate per base', 
        'Deletion average length', 
        'Insertion rate per base', 
        'Insertion average length', 
        'MULTI-MAPPING READS:', 
        'Number of reads mapped to multiple loci', 
        '% of reads mapped to multiple loci', 
        'Number of reads mapped to too many loci', 
        '% of reads mapped to too many loci', 
        'UNMAPPED READS:', 
        'Number of reads unmapped: too many mismatches', 
        '% of reads unmapped: too many mismatches', 
        'Number of reads unmapped: too short', 
        '% of reads unmapped: too short', 
        'Number of reads unmapped: other', 
        '% of reads unmapped: other', 
        'CHIMERIC READS:', 
        'Number of chimeric reads', 
        '% of chimeric reads'])])
        temp.loc['Sample'] = [sample]
        temp.columns = temp.loc['Sample']
        df_list.append(temp)
    # merge tables and save the merged output
    merged = pd.concat(df_list, axis=1)
    merged.loc['Uniquely mapped reads %'] = merged.loc['Uniquely mapped reads %'].str.rstrip("%").astype(float)
    merged.loc['% of reads mapped to multiple loci'] = merged.loc['% of reads mapped to multiple loci'].str.rstrip("%").astype(float)
    merged.loc['% of reads mapped to too many loci'] = merged.loc['% of reads mapped to too many loci'].str.rstrip("%").astype(float)
    merged.loc['Mapping Rate'] = (merged.loc['Uniquely mapped reads %'] + merged.loc['% of reads mapped to multiple loci'] + merged.loc['% of reads mapped to too many loci']) / 100
    merged.loc['Unique Rate of Mapped'] = ((merged.loc['Uniquely mapped reads %'] / 100) / merged.loc['Mapping Rate'])
    merged.to_csv((options.TSV), sep="\t")

##############################################################################

if __name__ == '__main__':

    try:
        # parse the command-line arguments
        options = parse_arguments().parse_args()

        # set up logging during the execution
        formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s\
                                      - %(message)s",
                                      datefmt="%d-%b-%Y %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger = logging.getLogger('uniprot_to_json')
        logger.setLevel(logging.getLevelName(options.verbosity))
        logger.addHandler(console_handler)
        if options.logfile is not None:
            logfile_handler = logging.handlers.RotatingFileHandler(
                options.logfile, maxBytes=50000, backupCount=2)
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
        logger.info("Successfully finished in {hours} hour(s) \
{minutes} minute(s) and {seconds} second(s)",
                    hours=int(hours),
                    minutes=int(minutes),
                    seconds=int(seconds) if seconds > 1.0 else 1)
    # log the exception in case it happens
    except Exception as e:
        logger.exception(str(e))
        raise e