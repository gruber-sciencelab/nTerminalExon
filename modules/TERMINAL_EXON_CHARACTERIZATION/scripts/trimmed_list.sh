#!/bin/bash
# -----------------------------------------------------------------------------
# Read in the parameters
# -----------------------------------------------------------------------------
usage()
{
cat << EOF
usage: $0 options
OPTIONS:
   -i                  The txt files.
   -r                  The results file with compressed info.
   -o                  The results file with descompressed info.
   -p                  The path to trimmed files.
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
txt_files=""
results_file_gz=""
results_file=""
trimmed_path=""

unset txt_files
unset results_file_gz
unset results_file
unset trimmed_path

# -----------------------------------------------------------------------------
# Declare input variables (OPERATIVE MODE)
# -----------------------------------------------------------------------------
while getopts i:r:o:p: opt
do
   case "$opt" in
      i) txt_files=$OPTARG;;
      r) results_file_gz=$OPTARG;;
      o) results_file=$OPTARG;;
      p) trimmed_path=$OPTARG;;
   esac
done

# _____________________________________________________________________________
# -----------------------------------------------------------------------------
# check if we got an argument
if [ "$txt_files" == "" ] || [ "$results_file_gz" == "" ] || [ "$results_file" == "" ] || [ "$trimmed_path" == "" ] ; then
    usage
    exit -1
fi

# _____________________________________________________________________________
# -----------------------------------------------------------------------------
# Give some feedback to the user on which files and directories are used
# -----------------------------------------------------------------------------
echo "________________________________________________________________________"
echo "------------------------------------------------------------------------"
echo "The txt file that is going to be read: ${txt_files}"
echo "The txt file with compressed information: ${results_file_gz}"
echo "The txt file with uncompressed information: ${results_file}"
echo "The directory from thw files are going to be analyzed: ${trimmed_path}"
echo "------------------------------------------------------------------------"

while read line
        do
        if [[ $line == *"single"* ]]
         then
            sample=$(cut -d : -f1 <<< $line)
            name=${sample//.bam/}
            echo "${trimmed_path}/$name._.fastq.gz" > ${results_file_gz}
            echo "${trimmed_path}/$name._.fastq" > ${results_file}
        elif [[ $line == *"paired_unstranded"* ]]
         then
            sample=$(cut -d : -f1 <<< $line)
            name=${sample//.bam/}
            echo "${trimmed_path}/$name.R.fastq.gz" > ${results_file_gz}
            echo "${trimmed_path}/$name.R.fastq" > ${results_file}
        elif [[ $line == *"paired_stranded_first"* ]]
         then
            sample=$(cut -d : -f1 <<< $line)
            name=${sample//.bam/}
            echo "${trimmed_path}/$name.R.fastq.gz" > ${results_file_gz}
            echo "${trimmed_path}/$name.R.fastq" > ${results_file}
        elif [[ $line == *"paired_stranded_second"* ]]
         then
            sample=$(cut -d : -f1 <<< $line)
            name=${sample//.bam/}
            echo "${trimmed_path}/$name.F.fastq.gz" > ${results_file_gz}
            echo "${trimmed_path}/$name.F.fastq" > ${results_file}
        fi
        done < ${txt_files}