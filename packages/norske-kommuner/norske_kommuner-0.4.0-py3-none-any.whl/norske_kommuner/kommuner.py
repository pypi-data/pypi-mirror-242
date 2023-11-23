from norske_kommuner.models import FylkerKommunerFull, KomFull
from collections import Counter
import json
import csv
from typing import Dict
from importlib import resources as impresources
from norske_kommuner import resources

class KommuneWithOrg(KomFull):
    orgnr: None | int


json_path = impresources.files(resources).joinpath('fylkeskommuner.json') 
csv_path = impresources.files(resources).joinpath('1236.csv') 

API_URL = 'https://ws.geonorge.no/kommuneinfo/v1/'
ORG_URL = 'https://www.ssb.no/klass/klassifikasjoner/582/korrespondanser/1236'

with impresources.as_file(json_path) as file:
    raw_json = file.read_text()

org_numbers = dict()
with impresources.as_file(csv_path) as file:
    raw_csv = file.read_bytes().decode('utf-8', errors='ignore')
    reader = csv.DictReader(raw_csv.splitlines(), delimiter=';')
    for row in reader:
        org_number = int(row['sourceCode'])
        kommune_number = row['targetCode']
        org_numbers[kommune_number] = org_number


kommuner_pydantic = [FylkerKommunerFull.model_construct(**i) for i in json.loads(raw_json)]
kommuner_flat = [KommuneWithOrg.model_construct(**k) for fylke in kommuner_pydantic for k in fylke.kommuner]
kommune_names_count = Counter([kommune.kommunenavn for kommune in kommuner_flat])
popular_names = {k for k, v in kommune_names_count.items() if v > 1}
kommuner: Dict[str, KommuneWithOrg] = dict()
for kommune in kommuner_flat:
    name = kommune.kommunenavn
    if name in popular_names:
        name = f'{name}_{kommune.fylkesnavn}'
    name = name.replace(' ', '').replace('-', '')
    org_number = org_numbers.get(kommune.kommunenummer, None)
    kommune.orgnr = org_number
    kommuner[name] = kommune
    


def get_kommune_by_nr(nr: str) -> KommuneWithOrg:
    return next((k for k in kommuner.values() if k.kommunenummer == nr), None)
