#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates how to connect to Cloud Bigtable and run some basic operations.

Prerequisites:

- Create a Cloud Bigtable cluster.
  https://cloud.google.com/bigtable/docs/creating-cluster
- Set your Google Application Default Credentials.
  https://developers.google.com/identity/protocols/application-default-credentials
"""

import datetime
import random
from google.cloud import bigtable

def main(project_id, instance_id, table_id):
    # [START connecting_to_bigtable]
    # The client must be created with admin=True because it will create a
    # table.
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    # [END connecting_to_bigtable]

    # [START creating_a_table]
    print('Creating the {} table.'.format(table_id))
    table = instance.table(table_id)
    table.delete()   #If you are re-running the script, the delete table can be invoked
    table.create()
    column_family_id = 'sensorcf1'
    sensorcf1 = table.column_family(column_family_id)
    sensorcf1.create()
    # [END creating_a_table]

    # [START writing_rows]
    print('Writing sample temperature data to the table.')
    column_id = 'sensordata'.encode('utf-8')
    dt = datetime.datetime(2017, 12, 01)
    end = datetime.datetime(2017, 12, 01, 23, 59, 59)
    step = datetime.timedelta(minutes=30)

    temp = []

    while dt < end:
        temp.append(dt.strftime('%Y%m%d%H%M%S'))
        dt += step

    for i, value in enumerate(temp):
        # For more information about how to design a Bigtable schema for
        # the best performance, see the documentation:
        #
        #     https://cloud.google.com/bigtable/docs/schema-design
        row_key = 'temp'+value
        row = table.row(row_key)
	temp_data = 'GARDEN' + str(random.randint(15, 35)) #Append a random temperature
        row.set_cell(
            column_family_id,
            column_id,
            temp_data.encode('utf-8'))
        row.commit()
    # [END writing_rows]

    # [START scanning_all_rows]
    print('Scanning for all temperature data:')
    partial_rows = table.read_rows()
    partial_rows.consume_all()

    for row_key, row in partial_rows.rows.items():
        key = row_key.decode('utf-8')
        cell = row.cells[column_family_id][column_id][0]
        value = cell.value.decode('utf-8')
        print('\t{}: {}'.format(key, value))
    # [END scanning_all_rows]

if __name__ == '__main__':
    #main(args.project_id, args.instance_id, args.table)
    main('gcp-cookbook','hometemp','temperature')
