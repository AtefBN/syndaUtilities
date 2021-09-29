"""
Script to generate intake-esm CSV files from synda database.
/!\ Make sure the synda daemon is stopped before launching this script to avoid corrupting the db /!\
"""
import dbtools
import regextools

conn = dbtools.connect()


def get_files_with_status(status='done', conn=conn):
    """
    notes
      - returns None if file not found
      - return type is File
    """
    files = []
    t = None

    c = conn.cursor()
    c.execute("select file_functional_id from File where status={}".format(status))
    rs = c.fetchone()
    while rs:
        files.append(dbtools.get_object_from_resultset(rs, dbtools.File))
        rs = c.fetchone()
    c.close()
    return t


def populate_csv_file(files):
    """
    From the list of files found in db, generate the csv rows from the file functional_id
    :param files:
    :return:
    """
    print('{} to process and add to CSV'.len(files))
    # removing .nc extension
    for f in files:
        f.replace('.nc', '')
    regextools.match_patterns_and_write_csv(files)
