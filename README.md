# nTerminalExon

1. Environment installation: CONDA + MAMBA

Appendix A: Download and installation of Miniconda3 and Mamba

To install the latest version of miniconda on a Linux systems please execute:

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source .bashrc

In addition, in order to execute workflows based on most-recent Snakemake versions it is essential to install Mamba alongside Conda. Mamba is basically Conda rewritten in C++ and it became the default front-end package manager utilized in Snakemake. For more information please visit this page.

Mamba has to be installed in the base environment with:

conda install -n base -c conda-forge mamba

In the case there is this error:

 ModuleNotFoundError: No module named 'chardet'

 pip install chardet charset_normalizer

2. crear conda environmente general

MAPP installation is therefore automatised and limitted to downloading the following repository (also possible with git clone command, provided Git version control system is available), navigating to the MAPP directory and running a shell script which will build the environment for the workflow. This may be achieved by the following command: bash scripts/create-conda-environment.sh

2. Download the resources

In order to run MAPP the user needs to provide general genomic information. The following are not part of a particular dataset and should be perceived as shared resources.
1A: Genome sequence and GTF-formatted annotation

MAPP requires species-specific genomic sequence and genomic annotation (in FASTA and GTF formats, respectively) that come from ENSEMBL servers and match the RNA-Seq data that will be analyzed. This repository contains a small bash script which may aid in the process of downloading these data for Homo sapiens:

bash scripts/download-ENSEMBL-resources.sh \
  --species hsa \
  --output-directory resources_ENSEMBL_hsa

For users who already have these genomic data this step is not necessary.
1B: Altas of PolyA-sites

MAPP requires that the user provides a BED-formatted list of representative PolyA sites. We include a small bash script that will automatically download the resource from our own curated atlas and re-format it according to further specifications.

bash scripts/download-polyA-atlas.sh \
  --species hsa \
  --output-directory ATLAS2_hsa

MAPP expects a BED-formatted list where the 5th column represents the number of protocols which support a given PolyA site and the name column encodes the exact coordinate of the representative site, as in the example below:

3. Creation of design file
We provide a teamplate, you have to fill in with bla bla bla

4. Create config file
conda activate nTE

crear el config file:

python scripts/create-main-config-file.py \
  --config-template configs/config_template.yml \
  --pipeline-configfile configs/config.yml

APPENDIX: how to download SRA samples

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