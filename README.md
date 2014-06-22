ultimatepiday.com
==============

1. Rename default_settings.cfg.example to default_settings.cfg and edit.

1. To create the schema for upd:
    ```py
    >>> import upd
    >>> upd.model.db.create_all(bind='upd')
    ```

1. Load sr26_mysql.062014.dmp.bz2 into mysql (db named sr26)
