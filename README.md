# nTerminalExon

# novel Terminal Exon

Identification of novel Terminal Exons analysis using TECtool. Please, download this repository with 'git clone' and follow the instructions.
Please be sure to execute the instructions in this directory folder. 

## Table of Contents

1. [Requirements](#requirements)
2. [Environment installation](#environment-installation)
3. [nTE conda environment](#nte-conda-environment)
4. [Download the required input files](#download-the-required-input-files)
5. [Create the design file](#create-the-design-file)
6. [Create the config file](#create-the-config-file)
7. [Start the analysis](#start-the-analysis)
8. [DEMO](#demo)

## Requirements

The nTerminalExon workflow can be used in both local and cluster computing setups. Researchers can opt for local execution on a single machine, suitable for smaller datasets, with a recommended system configuration of at least 16 cores and 100GB of RAM. Alternatively, utilizing a cluster environment enhances efficiency, particularly for larger-scale analyses, by harnessing parallel processing. 

## Environment installation: CONDA + MAMBA

To install the latest version of miniconda on a Linux systems please execute:

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source .bashrc
```
Mamba should be installed within the base environment as a requisite step.

```bash
conda install -n base -c conda-forge mamba
```

## nTE conda environment

The script file to create the conda nTE environment and the yml file with package dependencies are included. Create the environment:

```bash
bash scripts/create-conda-environment.sh
```
And activate it:

```bash
conda activate nTE
```

## Download the required input files

This analysis requires species-specific genomic sequence and annotation in FASTA and GTF formats from ENSEMBL servers. Included within this repository is a handy bash script that can assist in acquiring this data specifically for Homo sapiens:

```bash
bash scripts/download-ENSEMBL-resources.sh \
  --species hsa \
  --output-directory resources_ENSEMBL_hsa
```
A PolyA sites file is also required. The download process from [atlas] is also included:

```bash
bash scripts/download-polyA-atlas.sh \
  --species hsa \
  --output-directory ATLAS2_hsa
```

## Create the design file

In order to start the analysis, some basic technical and biological information has to be provided. In pursuit of this, a tsv file has to be submitted.
A template file is provided: *designfile_template.tsv*.

* Avoid using special characters such as period (.), pipe (|), and whitespace in the IDs of samples and in the condition columns.
* When filling the table, remember to input the paths for the forward reads in the "fq1" column and for the reverse reads in the "fq2" column. This rule applies even for single-end sequencing data. If the reads exclusively originate from the reverse strand, please leave the "fq1" field empty.
* "adapter1" pertains to reads found in the "fq1" column, while "adapter2" pertains to reads found in the "fq2" column.
* In the "library" column, you have the option to specify either "stranded" or "unstranded".

## Create the config file

The configuration details for this Snakemake pipeline are defined within the config.yml file. This generation relies on a template configuration file named *config_template.yml* (located in folder configs). It is the user's responsibility to adjust this template file manually. Don't leave any path without information, the process will not be completed successfully if it's not well done. After customizing the template to their satisfaction, they can generate a pipeline configuration file by executing a Python script tailored to it.

```bash
python scripts/create-main-config-file.py \
  --config-template configs/config_template.yml \
  --pipeline-configfile configs/config.yml
```

## Start the analysis

The analysis workflow comprises two distinct steps. The initial step is Preprocessing, encompassing essential rules to filter the sequencing files, adhering to the quality control guidelines outlined in the config file. Upon completing this phase, a new design file (design_table_quality_filtered.tsv) is generated, housing exclusively those samples that have successfully cleared the filter criteria. This file is produced as an output within the PREPROCESSING module.

To ensure the seamless completion of the entire process, review the text file containing output information and confirm the successful execution of 100% of the steps.

### Step 1: Sample preprocessing

```bash
# copy the snake preprocessing file
cp snakefiles/Snakefile_Step1_Preprocessing Snakefile
```

```bash
# Run the pipeline
nohup bash execution/run.sh \
  -c configs/config.yml \
  -e local \
  -n 8  \
  -t conda >& run_preprocessing.txt &
```
Once you have finished, you can delete the snakefile.

```bash
# remove the file
rm Snakefile
```
Once you've confirmed the completion of all steps and ensured the creation of the new design file in the preceding stage, you can now move on to Step 2.

### Step 2: Terminal Exon Characterization

The second step involves the necessary processes for analyzing the samples using the [TECtool] procedure. This will result in a tsv list (per fastq file) containing the newly identified terminal exons, accompanied by a pdf file containing sashimi plots of these terminal exons, and an enriched gtf file. A final step will consolidate the tsv results, creating a definitive file comprising the novel terminal exons per sample.

```bash
# copy the snake preprocessing file
cp snakefiles/Snakefile_Step2_TERMINAL_EXON_CHARACTERIZATION Snakefile
```

```bash
# Run the pipeline
nohup bash execution/run.sh \
  -c configs/config.yml \
  -e local \
  -n 8  \
  -t conda >& run_terminal_exon.txt &
```
Once you have finished, you can delete the snakefile.

```bash
# remove the file
rm Snakefile
```

# DEMO:

To start with the DEMO, start to download the sample files from SRA data repository. To create the environment:
```bash
bash scripts/create-conda-environment_sratoolkit.sh
```
And activate it:

```bash
conda activate sratoolkit
```
Download the samples SRR9274306 and SRR9274314 using prefetch *name of the sample* and fasterq-dump *name of the sample*
We provide a design file with the information to start the analysts (*DEMO.tsv*). Please, modify the file including the paths of the fastq files, and use the file as a design file for this demo.
Once you have the samples, you can start the analyses following the steps described previously.

Parts of the code have been taken and/or adapted from the [MAPP] GitHub [repository]

[atlas]: https://polyasite.unibas.ch/atlas
[TECtool]: https://github.com/zavolanlab/TECtool
[MAPP]: https://www.biorxiv.org/content/10.1101/2022.01.09.475576v1
[repository]: https://github.com/gruber-sciencelab/MAPP
