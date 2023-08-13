# nTerminalExon

# novel Terminal Exon

Identification of novel Terminal Exons analysis using TECtool

## Table of Contents

1. [Environment installation](#environment-installation)
2. [nTE conda environment](#nte-conda-environment)
3. [Execution test](#execution-test)
4. [Workflow execution](#workflow-execution)
5. [Appendix A: Download and installation of Miniconda3 and Mamba](#appendix-a-download-and-installation-of-miniconda3-and-mamba)


## Environment installation: CONDA + MAMBA

To install the latest version of miniconda on a Linux systems please execute:

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source .bashrc
```

In addition, in order to execute workflows based on most-recent Snakemake versions it is essential to install Mamba alongside Conda. Mamba is basically Conda rewritten in C++ and it became the default front-end package manager utilized in Snakemake. For more information please visit this page.

Mamba has to be installed in the base environment with:

```bash
conda install -n base -c conda-forge mamba
```

In the case there is this error:

 ModuleNotFoundError: No module named 'chardet'

```bash
pip install chardet charset_normalizer
```

## nTE conda environment

```bash
bash scripts/create-conda-environment.sh
```

```bash
conda activate nTE
```

2. Download the resources

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
We provide a teamplate, you have to fill in with bla bla bla

4. Create config file
conda activate nTE

crear el config file:

python scripts/create-main-config-file.py \
  --config-template configs/config_template.yml \
  --pipeline-configfile configs/config.yml

APPENDIX 1: how to download SRA samples

MAPP installation is therefore automatised and limitted to downloading the following repository (also possible with git clone command, provided Git version control system is available), navigating to the MAPP directory and running a shell script which will build the environment for the workflow. This may be achieved by the following command: bash scripts/create-conda-environment_sratoolkit.sh

Explicar un poco como funciona, dirigir a sratoolkit github etc etc

DEMO:

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