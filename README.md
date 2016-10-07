# appengine_datastore_bigquery

This python project serves as a guide to automate the following workflow:

1. Backup Google App Engine (GAE) NDB datastore entities to Google Cloud Storage.
2. Refresh BigQuery tables using latest backup files in Cloud Storage.
3. Delete old backup entities and files.

## Schedule datastore backups via App Engine cron

Read the [official documentation](https://cloud.google.com/appengine/articles/scheduled_backups)
to schedule automated backups of datastore models/kinds to a Cloud Storage bucket.
Refer to cron.yaml for an example.

## Set up BigQuery

BigQuery is Google's SQL-like analytics platform. If you haven't done so already, create a dataset in
[BigQuery](https://bigquery.cloud.google.com/queries/nom-nom-now).
The dataset will serve as the namespace for tables materialized from the backup files.

## Get dependencies and configure access controls

* Make sure your appengine_config.py is set up with a vendor directory. [Official documentation](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_library).
* Install the cloudstorage client library into the vendor lib: `pip install GoogleAppEngineCloudStorageClient -t lib`
* On the permissions admin for your project in console.cloud.google.com, make sure your `<PROJECT>@appspot.gserviceaccount.com` service account has permissions to BigQuery.
* On the cloud storage page, click the "three dots" icon and grant access to your `<PROJECT>@appspot.gserviceaccount.com` service account.

## Configure backup script for your project.
