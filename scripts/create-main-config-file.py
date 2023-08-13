"""
###############################################################################
#
#   Creation of configuration file
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   MODIFICATION: Miguel_Barquin
#   AFFILIATION: University_of_Konstaz
#   CREATED: 20-03-2020
#   MODIFIED: 14-02-2023
#   CONTACT: miguel.barquin@uni-konstanz.de
#
###############################################################################
"""

# imports
import time
import logging
import logging.handlers
from argparse import ArgumentParser, RawTextHelpFormatter
import os
import glob
import yaml
import pandas as pd


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
        "--config-template",
        dest="template",
        required=True,
        help="Meta-config file for the snakemake pipeline.",
    )
    parser.add_argument(
        "--pipeline-configfile",
        dest="pipeline_configfile",
        required=True,
        help="Path for the output YAML config file of the nTE pipeline.",
    )
    return parser


##############################################################################


def generate_windows(size, up, down):
    """Generate encoding for the sliding windows."""
    windows = []
    s = -1 * up
    e = s + size
    while e <= down:
        windows.append((s, e))
        s = s + int(float(size) / 2.0)
        e = e + int(float(size) / 2.0)
    # convert to dirextory names
    windows_directories = []
    for win in windows:
        if win[0] < 0 and win[1] <= 0:  # upstream ss
            windows_directories.append(
                "u" + str(-1 * win[0]) + "to" + str(-1 * win[1]) + ".d0to0"
            )
        elif win[0] >= 0 and win[1] > 0:  # downstream ss
            windows_directories.append("u0to0.d" + str(win[0]) + "to" + str(win[1]))
        else:  # window goes through ss
            windows_directories.append(
                "u" + str(-1 * win[0]) + "to0.d0to" + str(win[1])
            )
    return windows_directories


def main():
    """Main body of the script."""

    # read the YAML config template
    with open(options.template, "r") as f:
        template = yaml.safe_load(f)

    # parse the samples design table
    design_table = pd.read_csv(template["analysis_design_table"], sep="\t")
    sample_IDs = design_table["sample"]

    # default directory name for the per-modules output
    default_output_dir_name = "output"

    # set the pipeline configfile path
    if os.path.isabs(options.pipeline_configfile):
        pipeline_configfile = options.pipeline_configfile
    else:
        pipeline_configfile = os.path.join(
            template["nTE_directory"], options.pipeline_configfile
        )

    # dynamicaly created entries:
    ##########################################################################
    
    TEC_sample_bam_dict = []
    for s in sample_IDs:
        bam_path = os.path.join(
            template["nTE_directory"],
            "modules",
            "PREPROCESSING",
            default_output_dir_name,
            "alignments",
            s,
            s + ".Aligned.out.sorted.bam",
        )
        TEC_sample_bam_dict.append('  "' + s + '": "' + bam_path + '"')
    TEC_sample_bam_dict = os.linesep.join(TEC_sample_bam_dict)

    TEC_sample_new_bam_dict = []
    for s in sample_IDs:
        bam_path = os.path.join(
            template["nTE_directory"],
            "modules",
            "TERMINAL_EXON_CHARACTERIZATION",
            default_output_dir_name,
            "alignments",
            s,
            s + ".Aligned.out.sorted.bam",
        )
        TEC_sample_new_bam_dict.append('  "' + s + '": "' + bam_path + '"')
    TEC_sample_new_bam_dict = os.linesep.join(TEC_sample_new_bam_dict)
    
    TEC_sample_bai_dict = []
    for s in sample_IDs:
        bai_path = os.path.join(
            template["nTE_directory"],
            "modules",
            "PREPROCESSING",
            default_output_dir_name,
            "alignments",
            s,
            s + ".Aligned.out.sorted.bam.bai",
        )
        TEC_sample_bai_dict.append('  "' + s + '": "' + bai_path + '"')
    TEC_sample_bai_dict = os.linesep.join(TEC_sample_bai_dict)

    TEC_sample_new_bai_dict = []
    for s in sample_IDs:
        bai_path = os.path.join(
            template["nTE_directory"],
            "modules",
            "TERMINAL_EXON_CHARACTERIZATION",
            default_output_dir_name,
            "alignments",
            s,
            s + ".Aligned.out.sorted.bam.bai",
        )
        TEC_sample_new_bai_dict.append('  "' + s + '": "' + bai_path + '"')
    TEC_sample_new_bai_dict = os.linesep.join(TEC_sample_new_bai_dict)

    if template["quality_check"]:
        updated_design_table = os.path.join(
            template["nTE_directory"],
            "modules",
            "PREPROCESSING",
            default_output_dir_name,
            "design_table_quality_filtered.tsv",
        )
    else:
        updated_design_table = template["analysis_design_table"]

    ##########################################################################

    config_string = f"""---

nTE_analysis_name: "{template["analysis_name"]}"
nTE_pipeline_directory: "{template["nTE_directory"]}"
nTE_pipeline_configfile: "{pipeline_configfile}"

### module: PREPROCESSING
PQA_scripts_dir: "{template["nTE_directory"]}/modules/PREPROCESSING/scripts"
PQA_outdir: "{template["nTE_directory"]}/modules/PREPROCESSING/{default_output_dir_name}"
PQA_adapters_sequences: "{template["nTE_directory"]}/modules/PREPROCESSING/resources/adapters.txt"
PQA_genomic_sequence: "{template["genomic_sequence"]}"
PQA_genomic_annotation: "{template["genomic_annotation"]}"
PQA_index: "{template["genomic_index"]}"
PQA_design_file: "{template["analysis_design_table"]}"
PQA_sjdbOverhang: {template["sjdbOverhang"]}
PQA_transcript_biotypes: "{template["transcript_biotypes"]}"
PQA_min_median_TIN_score: {template["min_median_TIN_score"]}
PQA_RNASeQC_min_mapping_rate: {template["RNASeQC_min_mapping_rate"]}
PQA_RNASeQC_min_unique_rate_of_mapped: {template["RNASeQC_min_unique_rate_of_mapped"]}
PQA_RNASeQC_min_high_quality_rate: {template["RNASeQC_min_high_quality_rate"]}
PQA_RNASeQC_max_intergenic_rate: {template["RNASeQC_max_intergenic_rate"]}
PQA_RNASeQC_max_rRNA_rate: {template["RNASeQC_max_rRNA_rate"]}
PQA_storage_efficient: {template["storage_efficient"]}

### module: TERMINAL_EXON_CHARACTERIZATION
TEC_scripts_dir: "{template["nTE_directory"]}/modules/TERMINAL_EXON_CHARACTERIZATION/scripts"
TEC_outdir: "{template["nTE_directory"]}/modules/TERMINAL_EXON_CHARACTERIZATION/{default_output_dir_name}"
TEC_alignment_files:
{TEC_sample_bam_dict}
TEC_mapped_samples_indices:
{TEC_sample_bai_dict}
TEC_new_mapped_samples:
{TEC_sample_new_bam_dict}
TEC_new_mapped_samples_indices:
{TEC_sample_new_bai_dict}
TEC_design_file: "{updated_design_table}"
TEC_genomic_sequence: "{template["genomic_sequence"]}"
TEC_genomic_annotation: "{template["genomic_annotation"]}"
TEC_index: "{template["genomic_index"]}"
TEC_pas_atlas: "{template["PAS_atlas"]}"
TEC_storage_efficient: {template["storage_efficient"]}
TEC_trimmed_fq: "{template["nTE_directory"]}/modules/PREPROCESSING/{default_output_dir_name}/tail_trimmed"
TEC_bam_path: "{template["nTE_directory"]}/modules/PREPROCESSING/{default_output_dir_name}/alignment"
...
"""

    with open(options.pipeline_configfile, "w") as outfile:
        outfile.write(config_string)


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
