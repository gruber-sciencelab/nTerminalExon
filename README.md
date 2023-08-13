# nTerminalExon

# novel Terminal Exon

Identification of novel Terminal Exons analysis using TECtool

## Table of Contents

1. [Environment installation](#environment-installation)
2. [nTE conda environment](#nte-conda-environment)
3. [Download the required input files](#download-the-required-input-files)


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

In the case you will have following error `ModuleNotFoundError: No module named 'chardet'`, install chardet package:

```bash
pip install chardet charset_normalizer
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

In order to analyze the data, some 

```bash
bash scripts/download-ENSEMBL-resources.sh \
  --species hsa \
  --output-directory resources_ENSEMBL_hsa
```

```bash
bash scripts/download-polyA-atlas.sh \
  --species hsa \
  --output-directory ATLAS2_hsa
```

3. Creation of design file
We provide a template, you have to fill in with bla bla bla

4. Create config file
conda activate nTE

crear el config file:

python scripts/create-main-config-file.py \
  --config-template configs/config_template.yml \
  --pipeline-configfile configs/config.yml

APPENDIX 1: how to download SRA samples

MAPP installation is therefore automatised and limitted to downloading the following repository (also possible with git clone command, provided Git version control system is available), navigating to the MAPP directory and running a shell script which will build the environment for the workflow. This may be achieved by the following command: bash scripts/create-conda-environment_sratoolkit.sh

Explicar un poco como funciona, dirigir a sratoolkit github etc etc

# DEMO:

## Step 1: Sample preprocessing

```bash
cp snakefile/Snakefile_Step1_Preprocessing Snakefile
# Run the pipeline
bash exection/run.sh
# rm Snakefile

```

## Step 1: Terminal Exon Characterization

```bash
cp snakefile/Snakefile_Step2_Terminal_exon_characterization Snakefile
# Run the pipeline
bash exection/run.sh
```

Muestras + creacion design file


1. Muestras + creacion design file
conda activate sratoolkit
prefetch sra bla bla bla bla

SRR9274314
SRR9274306


creacion design file

2. Descargar los archivos de referencia

3. Empezar el analisis
conda activate nTE
modificacmos el config file con los paths al design file y tambien a los archivos de referencia
creamos el config file

4. Empezamos el analisis
