# Models for datastore entities created by App Engine datastore backup jobs.

from google.appengine.ext import ndb


class AeBackupInformation(ndb.Model):
    """Model for _AE_Backup_Information containing datastore backup info."""
    name = ndb.StringProperty()
    kinds = ndb.StringProperty(repeated=True)
    namespaces = ndb.StringProperty(repeated=True)
    filesystem = ndb.StringProperty()
    start_time = ndb.DateTimeProperty()
    completed_jobs = ndb.StringProperty(repeated=True)
    complete_time = ndb.DateTimeProperty()
    orginal_app = ndb.StringProperty()
    gs_handle = ndb.TextProperty()
    destination = ndb.StringProperty()

    @classmethod
    def _get_kind(cls):
        return '_AE_Backup_Information'

    @classmethod
    def get_latest_backup(cls):
        """Gets the entity representing the most recent datastore backup."""
        backups = cls.query().fetch()
        if backups:
            return backups[-1]

    def get_kind_files(self):
        return AeBackupInformationKindFiles.query(ancestor=self.key).fetch()


class AeBackupInformationKindFiles(ndb.Model):
    """Model for _AE_Backup_Information_Kind_Files, backed up entity kinds."""
    files = ndb.StringProperty(repeated=True)

    @classmethod
    def _get_kind(cls):
        return '_AE_Backup_Information_Kind_Files'
