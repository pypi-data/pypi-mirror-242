# Requirements
- Python 3
- Numpy
- Pandas
- [Pysam](https://pypi.org/project/pysam/)
- [Cigar](https://pypi.org/project/cigar/)
- [Tqdm](https://pypi.org/project/tqdm/)

You can install these dependencies using pip, the Python package manager, by running the following command in your terminal: `pip install numpy pandas pysam cigar tqdm`

# Usage
1. Clone this repository:

```bach
git clone https://plmlab.math.cnrs.fr/cluzel/reads_processing.git
```

2. Install the required packages:

```bach
pip install numpy pandas pysam cigar tqdm
```

3. Run the program:

```bach
python start.py <path_to_bam-cram_file_or_directory> <path_to_reference_sequence> [-o <output_directory>] [-p <filter_percentage>] [-n <filter_number>]
```
where:
- `<path_to_bam-cram_file_or_directory>`: The path to the BAM/CRAM file or directory containing BAM/CRAM files to be analyzed.
- `<path_to_reference_sequence>`: The path to the reference sequence file.
- `-o <output_directory> (optional)`: The path to the output directory where the results will be saved. Default is the current directory.
- `-p <filter_percentage> (optional)`: [filter parameter] The percentage of reads,cover the region of the mutation, that must contain a mutation to be kept as a mutation. Default is 0.0.
- `-n <filter_number> (optional)`: [filter parameter] The number of reads that must contain a mutation to be kept as a mutation. Default is 0.

Example usage:

```bach
python start.py /path/to/bam-cram/files/ /path/to/reference.fasta -o /path/to/output/directory/ -p 0.01 -n 5
```
This will analyze all BAM/CRAM files in the `/path/to/bam-cram/files/` directory using the reference sequence in `/path/to/reference.fasta`. The results will be saved in the `/path/to/output/directory/` directory with mutations that are present in at least 1% of reads that cover the mutation, and mutations that are present in at least 5 reads. If the -o, -p, or -n options are not specified, the program will use the default values.

# Output format
The tool outputs three files for each input BAM/CRAM file:

- `Xsparse_<bam-cram_file_name>_filter<filter_per>_<filter_num>_<random_id>.csv`
- `Wsparse_<bam-cram_file_name>_filter<filter_per>_<filter_num>_<random_id>.csv`
- `mutations_index_<bam-cram_file_name>_filter<filter_per>_<filter_num>_<random_id>.csv`

The `<bam-cram_file_name>` and `<random_id>` values are generated automatically based on the input file name and a random number, respectively. The `<filter_per>` and `<filter_num>` values correspond to the filtering parameters specified by the user.

### mutations_index File:
This file contains all the mutations found in the input BAM/CRAM file that pass the filtering criteria. Each line represents a mutation and works as an index of mutations in the `Xsparse` file. 
The `mutations_index` file will look like:
```
Mutations
T6TC
C9A
A11G
A11T
AAA14A
A16G
A16AG
...
...
```
This is interpreted as follows:
- The mutation at index 0 is `T6TC`
- The mutation at index 4 is `AAA14A`

#### mutation encoding
The mutation encoding is as follows:
[ref base][position][alt base]

Be aware that the position [in reference sequence] is 1-based. For example:
- `T6TC` means that the mutation is a transition from T to C at position 6 (the position is 1-based). It is a substitution.
- `AAA14A` means that the mutation is a transition from AAA to A at position 14[in reference sequence]. It is a deletion.
- `A16AG` means that the mutation is a transition from A to AG at position 16[in reference sequence]. It is an insertion.


### xsparse File

The `Xsparse` file is the most important file as it contains the actual data. Each line represents a read.

The `Xsparse` file will look like this:
```
startIdx_mutations_Based,endIdx_mutations_Based,muts
0,4,
0,4,"0, 2"
0,4,"3,"
1,7,"1, 4"
2,7,"2, 5, 6"
...
...
```
This is interpreted as follows:
- In read 0, it covers the region from mutation 0 (T6TC) inclusive to mutation 4 (AAA14A) exclusive[it covers the region of mutations 0,1,2 and 3 but not mutation 4]. It has no mutations.
- In read 4, it covers the region from mutation 2 (A11G) inclusive to mutation 7 (A16AG) exclusive. The mutations 2, 5, and 6 are found in this read.


### Wsparse  File
The Wsparse file contains the weight of each read to store the data more efficiently. The Wsparse file looks like this:
```
Counts
2
1
1
1
5
...
...
```
This is interpreted as follows:
- Read 0 occurs 2 times in the data.
- Read 1 occurs 1 time in the data.
- Read 4 occurs 5 times in the data.









 


