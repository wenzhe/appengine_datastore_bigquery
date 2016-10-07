# appengine_datastore_bigquery

This guide is targeted at people with 1) python app engine projects that 2) use datastore and
3) want to automate the process of importing datastore data into Google BigQuery tables. The
following topics are covered:

1. Backup Google App Engine (GAE) NDB datastore entities to Google Cloud Storage.
2. Refresh BigQuery tables using latest backup files in Cloud Storage.
3. Delete old backup entities and files.

## Schedule datastore backups via App Engine cron

Read the [official documentation](https://cloud.google.com/appengine/articles/scheduled_backups)
to schedule automated backups of datastore models/kinds to a Cloud Storage bucket.
Refer to cron.yaml for an example.

## Set up BigQuery

If you haven't done so already, create a dataset in
[BigQuery](https://bigquery.cloud.google.com/queries/nom-nom-now).
The dataset will serve as the namespace for tables materialized from the backup files.

## Get dependencies and configure access controls

* Make sure your appengine_config.py is set up with a vendor directory. [Official documentation](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_library).
* Install the cloudstorage client into the vendor directory: `pip install GoogleAppEngineCloudStorageClient -t lib`
* On the permissions admin for your project in console.cloud.google.com, make sure your `<PROJECT>@appspot.gserviceaccount.com` service account has permissions for BigQuery.
* On the cloud storage page, click the "three dots" icon and grant your `<PROJECT>@appspot.gserviceaccount.com` service account access to the bucket where the backups will be stored.

## Configure script to load data from backup into BigQuery

 `load_bigquery.py` contains the request handler to be run via `cron.yaml`. It will materialize BigQuery tables using the  most recent datastore backups. It will also delete backups older than a certain age. Configure your webapp routes to use it.

`bigquery_lib.py` contains project, BigQuery and cloud storage configuration variables to customize for your project.
