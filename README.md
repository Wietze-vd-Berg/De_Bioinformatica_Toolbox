# Bioinformatica_Toolbox_Salmon
version 1.0, X-3-2025


Authors: Nicole Bovenga, Joris Deelstra, Wietze van den Berg, Vincent de Jong en Marit van Nuil
Date: 2/25/2025
Version: 1.0

Name: Opdracht_Toolbox_Salmon

Description:.

Installation:

Part 1: Miniconda
First, Miniconda needs to be installed.
You can also install the full Conda, but since we only need Bioconda, it’s unnecessary because the full Conda is quite large.
Everything in parentheses is an explanation and should not be executed!
Everything between <> is a physical button you need to press!

1. Go to www.anaconda.com/download

2. Install the Linux version for Python 3.12 64-Bit (x86) Installer.

3. Once installed, open the terminal.

4. cd Downloads (or the other folder where Miniconda was installed)

5. ls -l (check if the file is executable, if it doesn’t show -rwxr, it is not executable, follow steps 3 and 4 if needed)

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

Part 2: Bioconda

Fortunately, we’ve now gotten through the most annoying part.

1. conda config --add channels bioconda

2. conda config --set channel_priority strict

This will install Bioconda.

Part 3: Salmon

Now, you can finally install Salmon!

1. conda create -n salmon salmon

This installs Salmon and creates a custom environment called salmon.
To activate and deactivate this environment, use the following commands:

1. conda activate salmon

2. conda deactivate


Usage:
Any and all instructions on how to use this package go here. Possibly also some explanation on
how to interpret the output.

Support:
If users run into trouble/find a bug, who do they contact?
(Generally, you just want to put your own email adress here)

Acknowledgment:
Here you can mention/thank anyone who helped you out while making this project.
If you make something for an institute/company you can also mention them here.

### REQUIREMENTS/VOLGORDE README

1. Titel
2. versie+datum
3. omschrijving
4. systeem requirements
5. instalatie
6. cmd line voorbeelden
7. support
8. referenties

(zie blackboard voor meer info)
