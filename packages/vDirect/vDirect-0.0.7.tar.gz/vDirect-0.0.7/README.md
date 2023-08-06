# VDirect

VDirect is a user friendly tool to retrieve information from the VOGDB-API. It is a utility that builds URLs and sends requests to the server. <br>
Functionality includes searching for species, proteins and virus orthologous groups (VOGs) objects, as well as getting more detailed information about these objects.
Fetching Multiple Sequence Alignments (MSA) and Hidden Markov Matrices (HMM) is possible for each VOG, and Aminoacid and Nucleotide Sequences can be fetched for proteins.

## Dependencies:
You can install the dependencies with
```bash
pip install argparse
pip install requests
```

## Installation
vDirect can be installed with:
```bash
pip install vDirect
```

## Using the VOGDB-API with vDirect

Below is the search hierarchy: first specify vsearch, vsummary or vfetch, then the subsequent parameters.<br/>
'-h' provides a list of the parameters that can be used for filtering.
```bash
vdirect      <base_url>    vsearch     species   species_search_parameters
                                        protein   protein_search_parameters
                                        vog       vog_search_parameters
                 
                            vsummary    species   species_ids
                                        protein   protein_ids
                                        vog       vog_ids
                 
                            vfetch      protein   faa   protein_ids
                                                  fna   protein_ids
                                        vog       hmm   vog_ids
                                                  msa   vog_ids
```
## Examples
```bash
vdirect  http://127.0.0.1:8000/ vsearch vog -pmax 10 -pmin 10
vdirect  http://127.0.0.1:8000/ vsearch species -n corona
vdirect  http://127.0.0.1:8000/ vsearch protein -n corona
vdirect  http://127.0.0.1:8000/ vfetch protein faa -id 1034149.YP_009198699.1
```
You can get summaries from the IDs returned by a search by using the shell syntax:
```bash
vdirect  http://127.0.0.1:8000/ vsummary vog -id $(vdirect -base http://127.0.0.1:8000/ vsearch vog -pmax 100 -pmin 100)
```
You can also set the base url as an environment variable with
```bash
base='http://127.0.0.1:8000/'
```
and then execute the command as
```bash
vdirect  $base vsummary vog -id $(vdirect $base vsearch vog -pmax 100 -pmin 100)
```
## Authors

Nikola Vinko*, Sigi Koizar*

*University of Vienna
