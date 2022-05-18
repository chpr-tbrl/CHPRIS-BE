from peewee import (
    CharField,
    DateTimeField,
    IntegerField,
    PrimaryKeyField,
    DateField,
    ForeignKeyField
)

from schemas.records.baseModel import BaseModel
from schemas.records.records import Records
from datetime import datetime

class Specimen_collection(BaseModel):
    specimen_collection_id = PrimaryKeyField()
    specimen_collection_records_id = ForeignKeyField(Records)
    specimen_collection_date = DateTimeField(default=datetime.now())
    specimen_collection_user_id = IntegerField()
    specimen_collection_1_date = DateField()
    specimen_collection_1_specimen_collection_type = CharField() #[‘sputum’, ‘csf’,‘lymph_node_aspirate’, ‘gastric_aspirate’, ‘urine’, ‘other’]
    specimen_collection_1_other = CharField()
    specimen_collection_1_period = CharField() #[‘spot’, ‘morning’, ‘n_a’]
    specimen_collection_1_aspect = CharField() #[‘mucopurulent’, ‘bloody’, ‘salivary’,‘n_a’]
    specimen_collection_1_received_by = CharField()
    specimen_collection_2_date = DateField()
    specimen_collection_2_specimen_collection_type = CharField() #[‘sputum’, ‘csf’,‘lymph_node_aspirate’, ‘gastric_aspirate’,‘urine’, ‘other’]
    specimen_collection_2_other = CharField()
    specimen_collection_2_period = CharField() #[‘spot’, ‘morning’, ‘n_a’]
    specimen_collection_2_aspect = CharField() #[‘mucopurulent’, ‘bloody’, ‘salivary’,‘n_a’]
    specimen_collection_2_received_by = CharField()
