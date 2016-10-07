# appengine_datastore_bigquery

This python project serves as a demo of how to automate the following workflow:

1. Backup Google App Engine(GAE) NDB datastore entities to Google Cloud Storage.
2. Refresh BigQuery tables using latest backup files in Cloud Storage.
3. Delete old backup entities and files.
