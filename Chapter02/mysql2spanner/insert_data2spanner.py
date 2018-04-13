# Imports the Google Cloud Client Library.
from google.cloud import spanner
from ast import literal_eval as make_tuple
import sys

def insert_data(instance_id, database_id, data_file):
    """Inserts sample data into the given database.
    The database and table must already exist and can be created using
    `create_database`.
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    dat = []

    f = open(data_file,"r") #opens file with name of "test.txt"
    for line in f:
	dat.append(line)
    dat = [x.strip() for x in dat] # Strips newline and spaces
    table_name = dat.pop(0)
    print('Table name: ' + table_name)
    dat = [make_tuple(x) for x in dat] # Makes tuples as expected by the insert function
    col_names = dat.pop(0)
    print('Column Names: ' + str(col_names))
    f.close() 

    with database.batch() as batch:
        batch.insert(
            table=table_name,
            columns=col_names,
	    values=dat)

# Instantiate a client.
spanner_client = spanner.Client()

# Your Cloud Spanner instance ID.
instance_id = 'org-dev'

# Get a Cloud Spanner instance by ID.
instance = spanner_client.instance(instance_id)

# Your Cloud Spanner database ID.
database_id = 'org'

# Get a Cloud Spanner database by ID.
database = instance.database(database_id)

data_file = sys.argv[1:].pop(0)
insert_data(instance_id, database_id, data_file)
print('Data inserted')


