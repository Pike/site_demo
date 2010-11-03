DEFAULT_DB_ALIAS = 'default'

class ReadOnlyRouter(object):
    def db_for_read(self, model, **hints):
        "Point all read operations on myapp models to 'status_read'"
        if model._meta.app_label == 'dmstatus':
            return 'status_read'
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations on myapp models to DEFAULT_DB_ALIAS,
        we want this installation to be read-only"""
        if model._meta.app_label == 'dmstatus':
            return DEFAULT_DB_ALIAS
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'dmstatus' or obj2._meta.app_label == 'dmstatus':
            return True
        return None

    def allow_syncdb(self, db, model):
        """syncdb on default so that accidental writes don't create db
        errors. They'll just be lost in nirvana.
        """
        if db == DEFAULT_DB_ALIAS:
            return model._meta.app_label == 'dmstatus'
        elif model._meta.app_label == 'dmstatus':
            return False
        return None
