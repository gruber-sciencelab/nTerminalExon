
#!/usr/bin/env bash

###############################################################################
#
#   Creation of SRAtoolkit conda environment
#
#   AUTHOR: Miguel_Barquin
#   AFFILIATION: University_of_Konstaz
#   CREATED: 20-03-2020
#   CONTACT: miguel.barquin@uni-konstanz.de
#
###############################################################################

CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
mamba env create --file "$CWD"/../env/environment_sratoolkit.yml
