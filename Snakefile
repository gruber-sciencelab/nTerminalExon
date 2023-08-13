##############################################################################
#
#   Snakemake pipeline: MAPP
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   AFFILIATION: Swiss_Institute_of_Bioinformatics
#   CONTACT: maciej.bak@unibas.ch
#   CREATED: 30-06-2020
#   LICENSE: Apache_2.0
#
##############################################################################
#hola
# imports
import sys
import os
import pandas as pd

# local rules
localrules: all

# create logging directory for the top-level rules of MAPP summary
os.makedirs(
    os.path.join(
        config["nTE_pipeline_directory"],
        "logs",
    ),
    exist_ok = True
)

def get_all_samples_IDs():
    """
    Selecting IDs from the design file (all samples)
    """
    design_table = pd.read_csv(config["TEC_design_file"], sep="\t")
    return list(design_table["sample"])

##############################################################################
### Target rule with final output of the pipeline
##############################################################################

rule all:
    """
    Gathering all output
    """
    input:
        TSV_new_design_table = expand(
            os.path.join(
                "{PQA_output_dir}",
                "design_table_quality_filtered.tsv"
            ),
            PQA_output_dir = config["PQA_outdir"]
        ),
        QC_plot = expand(
            os.path.join(
                "{PQA_output_dir}",
                "qc_plot.pdf"
            ),
            PQA_output_dir = config["PQA_outdir"]
        )

##############################################################################
### Include all MAPP modules:
##############################################################################

include: "modules/PREPROCESSING/Snakefile"