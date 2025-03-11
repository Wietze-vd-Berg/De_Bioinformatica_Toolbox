# Bioinformatica_Toolbox_Salmon
version 2.0, Date: 2/25/2025

Authors: Nicole Bovenga, Joris Deelstra, Wietze van den Berg, Vincent de Jong en Marit van Nuil
 
 
## Description
This tool and website help users analyze differences in gene expression between two RNA samples using Salmon, a wicked-fast and accurate RNA-seq quantification tool. [[1]](https://combine-lab.github.io/salmon/about/)
It allows the user to compare gene activity levels and understand how genes are expressed in different conditions.
Gene expression is the process where genetic information from DNA is used to produce RNA and proteins. By measuring gene expression, you can see which genes are active.
Salmon is a tool that quickly estimates gene expression levels from RNA-seq data. Instead of slowly aligning sequences to a genome, 
Salmon uses smart algorithms to quickly and accurately determine how much each gene is expressed. [[2]](https://github.com/COMBINE-lab/salmon)

Users upload RNA-sequencing files, and the tool processes them using Salmon to analyze gene expression.
They can then compare the RNA samples and explore differences. The tool generates visual reports that the user can download or export. [[3]](https://salmon.readthedocs.io/en/latest/salmon.html)

## Requirements
Machine with python 2.7 or higher. <br>
This guide is for Linux operating systems.

## Installation
### Part 1: Miniconda
This step can be skipped if you've already installed mini/ana-conda
```
First, Miniconda needs to be installed.
You can also install the full Conda, but since we only need Bioconda, it’s unnecessary because the full Conda is quite large.
Everything in parentheses is an explanation and should not be executed!
Everything between <> is a physical button you need to press!
 
1. Go to www.anaconda.com/download
 
2. Install the Linux version for Python 3.12 64-Bit (x86) Installer.
 
3. Once installed, open the terminal.
 
4. cd Downloads (or the other folder where Miniconda was installed)
 
5. ls -l (check if the file is executable, if it shows -rwxr, it is executable step 6 and 7 can be skipped)
 
6. chmod u+x <tab> (u = user, x adds the execute permission, tab for auto-complete, if tab doesn’t work, type the full name, mind the spelling!)
 
7. ls -l (check if -rwxr is correctly set)
 
Now Miniconda can be executed.
 
1. ./<tab> (miniconda)
 
2. Press <enter> (multiple times to go through all the documentation).
 
3. Press Q.
 
4. Yes.
 
5. Press <enter>.
 
The download of Miniconda will now begin.
yes (this will automatically start Conda when you open the terminal)
```
### Part 2: Bioconda
This step can be skipped if anaconda is already installed
 
```
Fortunately, we’ve now gotten through the most annoying part.
 
1. conda config --add channels bioconda
 
2. conda config --set channel_priority strict
 
This will install Bioconda.
```
### Part 3: Salmon
 
```
Now, you can finally install Salmon and creat a virtual environment!
 
1. conda create -n salmon salmon
 
This installs Salmon and creates a custom environment called salmon.
To activate and deactivate this environment, use the following commands:
 
1. conda activate salmon
 
2. conda deactivate
```
 
## Examples
Any and all instructions on how to use this package go here. Possibly also some explanation on
how to interpret the output.
 
## Support
If you run into a bug or an error, send a mail to nicolebovenga004@gmail.com
 
## References
 
[1]Combine Lab. (2025, februari 16). Salmon: About. https://combine-lab.github.io/salmon/about/  
 
[2]COMBINE-lab. (2025, februari 18). Salmon [GitHub-repository]. GitHub. https://github.com/COMBINE-lab/salmon 
 
[3]Salmon. (2025, februari 18). Salmon-documentatie. https://salmon.readthedocs.io/en/latest/salmon.html 
 
