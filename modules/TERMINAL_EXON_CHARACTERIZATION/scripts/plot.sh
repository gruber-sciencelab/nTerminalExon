#!/bin/bash
# -----------------------------------------------------------------------------
# Read in the parameters
# -----------------------------------------------------------------------------
usage()
{
cat << EOF
usage: $0 options
OPTIONS:
   -i                  The TSV.
   -g                  The genomic anottation file.
   -b                  The atlas bed file.
   -r                  The bam file.
   -o                  The output dir.
EOF
}

if [ $# -lt 1 ] ; then
    usage
    exit 1
fi

# _____________________________________________________________________________
# -----------------------------------------------------------------------------
# Declare input variables (DEBUG MODE)
# -----------------------------------------------------------------------------
dir_tsv=""
genome_file=""
atlas_file=""
bam_file=""
output_dir=""

unset dir_tsv
unset genome_file
unset atlas_file
unset bam_file
unset output_dir

# -----------------------------------------------------------------------------
# Declare input variables (OPERATIVE MODE)
# -----------------------------------------------------------------------------
while getopts i:g:o:b:r:o: opt
do
   case "$opt" in
      i) dir_tsv=$OPTARG;;
      g) genome_file=$OPTARG;;
      b) atlas_file=$OPTARG;;
      r) bam_file=$OPTARG;;
      o) output_dir=$OPTARG;;
   esac
done

# _____________________________________________________________________________
# -----------------------------------------------------------------------------
# check if we got an argument
if [ "$dir_tsv" == "" ] || [ "$genome_file" == "" ] || [ "$atlas_file" == "" ] || [ "$bam_file" == "" ]|| [ "$output_dir" == "" ]; then
    usage
    exit -1
fi

# _____________________________________________________________________________
# -----------------------------------------------------------------------------
# Give some feedback to the user on which files and directories are used
# -----------------------------------------------------------------------------
echo "________________________________________________________________________"
echo "------------------------------------------------------------------------"
echo "The tsv file: ${dir_tsv}"
echo "The genome annotation used: ${genome_file}"
echo "The poly-a atlas file: ${atlas_file}"
echo "The bam files: ${bam_file}"
echo "The directory to which the results will be written: ${output_dir}"
echo "------------------------------------------------------------------------"

tsv_file=${dir_tsv}/classified_as_terminal_with_probabilities.tsv

if [ -f "$tsv_file" ]; then
   plot_novel_exons.R \
   --gtf ${genome_file} \
   --polyasites ${atlas_file} \
   --bam ${bam_file} \
   --tectool_exons $tsv_file \
   --output_dir ${output_dir}
else 
    echo "$tsv_file does not exist."
fi