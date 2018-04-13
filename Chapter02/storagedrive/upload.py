import argparse
import hashlib
import datetime
from google.cloud import storage
from google.cloud import datastore

def create_client(project_id):
    return datastore.Client(project_id)

def add_drive_entry(client, gcs_filename, empid, tms):
    key = client.key('Drive')
    drive = datastore.Entity(
        key, exclude_from_indexes=['filekey'])
    drive.update({
        'created': datetime.datetime.utcnow(),
        'filekey': gcs_filename,
        'timestamp': tms,
        'empid': empid
    })
    client.put(drive)
    return drive.key

def list_drive_entries(client):
    query = client.query(kind='Drive')
    query.order = ['created']
    return list(query.fetch())
 
def main(project_id, file_name):
    empid="121659"  # An hardcoded employee ID
    client = storage.Client()
    # https://console.cloud.google.com/storage/browser/[bucket-id]/
    bucket = client.get_bucket('static_site') # Hardcoded bucket id
    hash_object = hashlib.md5(file_name.encode())
    hex_dig = hash_object.hexdigest()
    gcs_filename = hex_dig[:5]
    dt = datetime.datetime.now()
    tms = dt.strftime('%Y%m%d%H%M%S')
    gcs_filename = gcs_filename + "/" + tms + "/" + empid + "/" + file_name
    print('File name uploaded : ' + gcs_filename)
    blob2 = bucket.blob(gcs_filename)
    blob2.upload_from_filename(filename=file_name)
    ds_client = create_client(project_id)
    drive_key = add_drive_entry(ds_client, gcs_filename, empid, tms)
    print('Task {} added.'.format(drive_key.id))
    print('=== List of entries ===')
    print(list_drive_entries(ds_client))
    print('=======================')    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument(
    'file_name', help='Local file name')
    
    args = parser.parse_args()
    main(args.project_id, args.file_name)

