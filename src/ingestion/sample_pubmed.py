from Bio import Entrez
import json

Entrez.email = "kmoshehnaz@gmail.com"  # NCBI requires an email

ids = Entrez.read(Entrez.esearch(db="pubmed", term="machine learning",
                                 retmax=5, sort="date"))["IdList"]
print("IDs:", ids)

handle = Entrez.efetch(db="pubmed", id=",".join(ids), retmode="xml")
data = Entrez.read(handle)
json.dump(data, open("data/raw/sample_pubmed.json", "w"), indent=2, default=str)
print("saved")