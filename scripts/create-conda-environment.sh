
#!/usr/bin/env bash

###############################################################################
#
#   Creation of nTE conda environment
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

CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
mamba env create --file "$CWD"/../env/environment.yml
