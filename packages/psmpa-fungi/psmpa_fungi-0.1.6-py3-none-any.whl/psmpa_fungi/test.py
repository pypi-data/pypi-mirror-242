from os import path

project_dir = path.dirname(path.abspath(__file__))

# psmpa2 default files directory
default_psmpa2_dir = path.join(project_dir, "default_files")

default_psmpa2_blast_database = path.join(default_psmpa2_dir, "blast_db", "rna")

