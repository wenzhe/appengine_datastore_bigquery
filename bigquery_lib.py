# Library for loading datastore backups into BigQuery and deleting old backups.

import cloudstorage
import datetime
import logging
import models
from google.appengine.ext import ndb
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

# Configure these settings for your particular project.
PROJECT_ID = 'app-engine-project-id'
BIGQUERY_DATASET = 'bigquery-dataset'
CLOUD_STORAGE_BUCKET = 'cloud-storage-datastore-backup-bucket'


def create_service():
    """Creates reusable bigquery service authenticated with app credentials."""
    credentials = GoogleCredentials.get_application_default()
    return build('bigquery', 'v2', credentials=credentials)


def load_backup_into_bigquery(bigquery_service, backup_key, table):
    """Loads a datastore model backup on cloud storage into a BigQuery table.

    Args:
      bigquery_service: BigQuery API service to call to perform the load.
      backup_key: String URL safe key of the datastore backup entity.
      table: String name of the backed up table to be loaded.

    Returns:
      Job representing the BigQuery load operation.
    """
    source_uri = 'gs://{bucket}/{key}.{table}.backup_info'.format(
        bucket=CLOUD_STORAGE_BUCKET, key=backup_key, table=table)
    job_data = {
        'configuration': {
            'load': {
                'datasetId': BIGQUERY_DATASET,
                'projectId': PROJECT_ID,
                'tableId': table,
                'sourceFormat': 'DATASTORE_BACKUP',
                'sourceUris': [source_uri],
                # If BigQuery table already exists, it will be overwritten.
                'writeDisposition': 'WRITE_TRUNCATE',
                'destinationTable' : {
                    'projectId': PROJECT_ID,
                    'datasetId': BIGQUERY_DATASET,
                    'tableId'  : table,
                },
            },
        },
    }

    return bigquery_service.jobs().insert(
        projectId=PROJECT_ID, body=job_data).execute()


def delete_old_backups(max_days_age=14):
    """Deletes old backups from both datastore and cloud storage.

    Args:
      max_days_age: Integer days threshold for keeping backups.
    """
    now = datetime.datetime.utcnow()
    delete_max_age = now - datetime.timedelta(days=max_days_age)
    _delete_backups_from_datastore(delete_max_age)
    _delete_backups_from_cloud_storage(delete_max_age)


def _delete_backups_from_datastore(delete_max_age):
    """Deletes backup entities in datastore older than specified datetime."""
    keys_to_delete = []
    for backup_info in models.AeBackupInformation.query().fetch():
        if backup_info.complete_time < delete_max_age:
            keys_to_delete.append(backup_info.key)
            logging.info('Deleting backup info %s', backup_info.key)
            kind_files = backup_info.get_kind_files()
            for kind_file in kind_files:
                keys_to_delete.append(kind_file.key)
                logging.info('Deleting backup kind file %s', kind_file.key)
    if keys_to_delete:
        ndb.delete_multi(keys_to_delete)


def _delete_backups_from_cloud_storage(delete_max_age):
  """Deletes backup files in cloud storage older than specified datetime."""
  bucket_results = cloudstorage.listbucket('/{}/'.format(CLOUD_STORAGE_BUCKET))
  for row in bucket_results:
      if datetime.datetime.utcfromtimestamp(int(row.st_ctime)) < delete_max_age:
          cloudstorage.delete(row.filename)
