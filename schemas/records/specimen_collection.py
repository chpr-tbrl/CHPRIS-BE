from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import PrimaryKeyField
from peewee import DateField
from peewee import ForeignKeyField

from schemas.records.baseModel import BaseModel
from schemas.records.records import Records
from datetime import datetime

class Specimen_collections(BaseModel):
    specimen_collection_id = PrimaryKeyField()
    specimen_collection_records_id = ForeignKeyField(Records)
    specimen_collection_date = DateTimeField(default=datetime.now)
    specimen_collection_user_id = IntegerField()
    specimen_collection_1_date = DateField()
    specimen_collection_1_specimen_collection_type = CharField() #[‘sputum’, ‘csf’,‘lymph_node_aspirate’, ‘gastric_aspirate’, ‘urine’, ‘other’]
    specimen_collection_1_other = CharField(null=True)
    specimen_collection_1_period = CharField(null=True) #[‘spot’, ‘morning’, ‘n_a’]
    specimen_collection_1_aspect = CharField(null=True) #[‘mucopurulent’, ‘bloody’, ‘salivary’,‘n_a’]
    specimen_collection_1_received_by = CharField()
    specimen_collection_2_date = DateField(null=True)
    specimen_collection_2_specimen_collection_type = CharField(null=True) #[‘sputum’, ‘csf’,‘lymph_node_aspirate’, ‘gastric_aspirate’,‘urine’, ‘other’]
    specimen_collection_2_other = CharField(null=True)
    specimen_collection_2_period = CharField(null=True) #[‘spot’, ‘morning’, ‘n_a’]
    specimen_collection_2_aspect = CharField(null=True) #[‘mucopurulent’, ‘bloody’, ‘salivary’,‘n_a’]
    specimen_collection_2_received_by = CharField(null=True)
