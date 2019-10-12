# Detection of RNA Outlier Pipeline
[![Pipeline status](https://travis-ci.org/mumichae/drop.svg?branch=master)](https://travis-ci.org/mumichae/drop)
[![Version](https://img.shields.io/badge/Version-0.9.0-green.svg)](https://github.com/gagneurlab/mumichae/drop/master)
<img src="drop_sticker.png" alt="drop logo" width="200" class="center"/>

## Installation
You can install `drop` from github using `pip`. For this you need to recursively clone the repository with all its submodules first.
```
git clone https://github.com/mumichae/drop.git --recurse-submodules
cd drop
pip install -e .
```

## Start a new project
A new `drop` project needs to be initialized, which creates the necessary files.
```
cd <new/project/path>
drop init
```
Fill in the paths to the raw data as well as different settings for the config file. Create the sample annotation file according to ... Once these files are set up, you can look the complete workflow using
```
snakemake -n
```
This shows you the rules of all subworkflows. Omit `-n` if you are sure that you want you execute all printed rules. You can also invoke single workflows explicitly e.g. for aberrant splicing with 
```
snakemake aberrant_expression -n
```
