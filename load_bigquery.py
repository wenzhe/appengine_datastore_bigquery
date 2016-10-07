import bigquery_lib
import models
import webapp2


class LoadBigQueryHandler(webapp2.RequestHandler):
    """Cron handler to load latest datastore backups into BigQuery tables."""

    def get(self):
        bigquery_service = bigquery_lib.create_service()
        latest_backup = models.AeBackupInformation.get_latest_backup()
        if not latest_backup:
            return
        for row in latest_backup.get_kind_files():
            bigquery_lib.load_backup_into_bigquery(
                bigquery_service=bigquery_service,
                backup_key=latest_backup.key.urlsafe(),
                table=row.key.id())
        bigquery_lib.delete_old_backups()
        self.response.write('BigQuery table loads have been started.')
