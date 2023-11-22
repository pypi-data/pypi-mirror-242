#!/usr/bin/env python


from os import path

project_dir = path.dirname(path.abspath(__file__))

# psmpa-fungi default files directory
default_psmpa_fungi_dir = path.join(project_dir, "default_files", "psmpa_fungi")

default_psmpa_fungi_blast_database = path.join(default_psmpa_fungi_dir, "blast_db", "ref18S")

default_psmpa_fungi_database = {"default": path.join(default_psmpa_fungi_dir, "psmpa_fungi_database_default.tsv.gz")}

# default_psmpa_fungi_database_copy_number = path.join(default_psmpa_fungi_dir, 'psmpa2_database_16S_count.tsv.gz')

# default_psmpa_fungi_database_lineage = path.join(default_psmpa_fungi_dir, 'psmpa2_database_lineage.tsv.gz')

