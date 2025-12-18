import sqlite3 
import os

path = os.path.abspath('data/DutchSnomedCT.sqlite3') # insert your SNOMED CT directory
out_path = "snomed_is_a_inferred_labels.ttl" # insert your output path

if not os.path.exists(path):
    raise IOError(
        'Database %s not available.'
        % path)

db_connection = sqlite3.connect(path, check_same_thread=False)

REL_TABLE = "Relationship"  
IS_A = 116680003
CHAR_INFERRED = 900000000000011006  # inferred taxonomy
CHUNK = 100_000        

SQL = f"""
SELECT DISTINCT sourceId, destinationId
FROM {REL_TABLE}
WHERE active = 1
  AND typeId = ?
  AND characteristicTypeId = ?
"""

cursor = db_connection.cursor()

cursor.execute(SQL, (IS_A, CHAR_INFERRED))

with open(out_path, "w", encoding="utf-8") as f:
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    f.write("@prefix sct:  <http://snomed.info/id/> .\n\n")

    while True:
        rows = cursor.fetchmany(CHUNK)
        if not rows:
            break
        for src, dst in rows:
            f.write(
                f"sct:{src} "
                f"rdfs:subClassOf "
                f"sct:{dst} .\n"
            )

cursor.close()
db_connection.close()
print(f"Wrote {out_path}")