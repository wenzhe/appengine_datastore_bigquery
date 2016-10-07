# appengine_datastore_bigquery

This is a guide on how to automate the loading of datastore data into BigQuery in python App Engine.
Steps covered:

1. Backup Google App Engine NDB datastore entities to Google Cloud Storage.
2. Refresh BigQuery tables using latest backup files in Cloud Storage.
3. Delete old backup entities and files.

## Schedule datastore backups via App Engine cron

Read the [official documentation](https://cloud.google.com/appengine/articles/scheduled_backups)
to schedule automated backups of datastore models into Cloud Storage bucket.
Refer to `cron.yaml` for an example.

## Set up BigQuery

If you haven't done so already, enable [BigQuery](https://bigquery.cloud.google.com/queries/nom-nom-now)
in your project and create a dataset.
The dataset will serve as the namespace for tables materialized from datastore backups.

## Get dependencies and configure access controls

* Make sure your appengine_config.py is set up with a vendor directory. [Official documentation](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27#installing_a_library).
* Install the Cloud Storage client library into the vendor directory: `pip install GoogleAppEngineCloudStorageClient -t lib`
* On the permissions admin for your project in console.cloud.google.com, make sure your `<PROJECT>@appspot.gserviceaccount.com` service account has permissions for BigQuery.
* On the cloud storage page, click the "three dots" icon and grant your service account access to the bucket where the backups will be saved.

## Configure script to load data from backup into BigQuery

 `load_bigquery.py` contains the request handler to be run via `cron.yaml`. It will materialize BigQuery tables using the  most recent datastore backups. It will also delete backups older than a certain age.

Configure the three variables at the top of `bigquery_lib.py` for your project.

## License

Released under the MIT License, see `LICENSE`.
