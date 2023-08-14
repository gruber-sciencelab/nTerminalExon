# nTerminalExon

# novel Terminal Exon

Identification of novel Terminal Exons analysis using TECtool. Please, download this repository with 'git clone' and follow the instructions.

## Table of Contents

1. [Environment installation](#environment-installation)
2. [nTE conda environment](#nte-conda-environment)
3. [Download the required input files](#download-the-required-input-files)
4. [Create the design file](#create-the-design-file)


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

The configuration details for this Snakemake pipeline are defined within the config.yml file. This generation relies on a template configuration file named *config_template.yml* (located in folder configs). It is the user's responsibility to manually adjust this template file. After customizing the template to their satisfaction, they can generate a pipeline configuration file by executing a Python script tailored to it.

```bash
python scripts/create-main-config-file.py \
  --config-template configs/config_template.yml \
  --pipeline-configfile configs/config.yml
```

## Start the analysis

Start with Part 1 analysis

### Step 1: Sample preprocessing

```bash
# copy the snake preprocessing file
cp snakefile/Snakefile_Step1_Preprocessing Snakefile
# Run the pipeline
nohup bash execution/run.sh \
  -c configs/config.yml \
  -e local \
  -n 8  \
  -t conda >& run_preprocessing.txt &
# remove the file
rm Snakefile
```
Once you have finished, you can delete the snakefile.

```bash
# remove the file
rm Snakefile
```
Start with Part 2 analysis

### Step 2: Terminal Exon Characterization

```bash
# copy the snake preprocessing file
cp snakefile/Snakefile_Step2_TERMINAL_EXON_CHARACTERIZATION
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
Download the samples SRR9274306 and SRR9274306 using prefetch *name of the sample* and fasterq-dump *name of the sample*

Once you have the samples, you can start the analysys following the steps described previously.

[atlas]: https://polyasite.unibas.ch/atlas
