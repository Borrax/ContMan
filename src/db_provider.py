import json
import os


class DbProvider():
    __db_path = '../db/db.json'
    __json_indent = 2

    def __get_default_dbobj():
        return {
            'games': [],
            'movies': [],
            'books': []
        }

    def get_db_json():
        db_path = DbProvider.__db_path

        try:
            db_file = open(db_path, 'r')
        except FileNotFoundError:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            db_file = open(db_path, 'w')
            data_str = json.dumps(DbProvider.__get_default_dbobj(),
                                  indent=DbProvider.__json_indent)

            db_file.write(data_str)
            db_file.close()
            db_file = open(db_path, 'r')

        json_data = json.load(db_file)
        db_file.close()

        return json_data

    def rewrite_db(json_obj):
        db_file = open(DbProvider.__db_path, 'w')
        data_str = json.dumps(json_obj, indent=DbProvider.__json_indent)

        db_file.write(data_str)
        db_file.close()