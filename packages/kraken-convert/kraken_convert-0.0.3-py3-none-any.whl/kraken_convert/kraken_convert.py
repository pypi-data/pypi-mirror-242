
from kraken_convert import to_dot
from kraken_convert import mapping_engine
from kraken_convert import json_helper as json
import time



def convert(records, map):
    """Given records and a map, converts records
    """

    # Cycle through records and transform using mapping
    records = records if isinstance(records, list) else [records]
    mapped_records = []
    for record in records:
        mapped_record = mapping_engine.mapping_engine(record, map)
        mapped_record = mapped_record if isinstance(mapped_record, list) else [mapped_record]
        mapped_records += mapped_record
       
    return mapped_records
    