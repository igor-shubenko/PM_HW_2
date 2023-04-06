import json
from collections import defaultdict
import copy


class FileReaderAndWriter:
    """Class provides methods for reaing data from file and write data in file,
    recieves as a parametr path to file """
    def __init__(self, path: str):
        self._path = path
        self._data = None

    def read(self):
        with open(self._path, 'r', encoding='utf-8') as f:
            self._data = f.read()

    def write(self):
        with open(self._path, 'w', encoding='utf-8') as f:
            f.write(self._data)


class JsonLinesConverter(FileReaderAndWriter):
    """Class provides methods for converting json-lines string
    to list of dicts and from list of dicts to json-lines string"""
    def json_to_dict(self):
        self._data = [json.loads(line) for line in self._data.split('\n')] if self._data else []

    def dict_to_json(self):
        self._data = '\n'.join([json.dumps(line) for line in self._data])


class DatabaseImitation(JsonLinesConverter):
    """Class provides methods for working with .jsonl file"""
    def create_db(self):
        """Creates temp identificators for records for futher working with them"""
        self._db = defaultdict(list)
        for record in self._data:
            if record:
                self._db[record['name']+str(record['time_created'])] += [record]

    def load_data(self):
        self.read()
        self.json_to_dict()
        self.create_db()

    def dump_data(self):
        self._data = [record for v in self._db.values() for record in v]
        self.dict_to_json()
        self.write()


class DataWorker(DatabaseImitation):
    """Class provides CRUD methods for working with data"""
    def get_record(self, ind):
        """Returns record by unique identificator or all records(if ind=='all')"""
        self.load_data()

        if ind == 'all':
            return self._data if self._data else {"Message": "No records."}

        return self._db[ind] if self._db[ind] else {"message": "Record not found"}

    def update_record(self, ind, data):
        """Updades record bu unique identificator, if it exists"""
        if not data:
            return {"Error": "No data for update"}

        self.load_data()

        if ind not in self._db:
            return {"Error": "Record not found"}

        data.pop('name', None)
        data.pop('time_created', None)
        old_rec = copy.deepcopy(self._db[ind])
        for rec in self._db[ind]:
            rec.update(data)
        self.dump_data()

        return {"Updated": {'old record': old_rec, "new record": self._db[ind]}}

    def create_record(self, data):
        """Creates new record, if unique identificator does not exist"""
        if not all(map(lambda x: x in data.keys(), ('name', 'time_created', 'age'))):
            return {"Error": "Missing one or both of required fields: 'name', 'time_created', 'age'"}

        self.load_data()
        record_id = data['name'] + str(data['time_created'])
        if record_id in self._db.keys():
            return {"Error": "Record already exists"}

        self._db[record_id] = [data]
        self.dump_data()

        return {"Record created": data}

    def delete_record(self, ind):
        """Deletes record by identificator or all records(if ind=='all')"""
        if ind == 'all':
            self._db = {}
            self.dump_data()
            return {"Message": "All records deleted!"}

        self.load_data()
        record = self._db[ind][:]
        del self._db[ind]
        self.dump_data()

        return {"Deleted": record} if record else {"Message": "Nothing to delete, record not exists"}

class DataWorkerByIndex(JsonLinesConverter):
    """Provedes methods for working with file data by identificator,
        identificator - number of row in file, beginning from 0"""
    def load_data(self):
        self.read()
        self.json_to_dict()

    def dump_data(self):
        self.dict_to_json()
        self.write()

    def validate_index(self, ind):
        if not ind.isdigit():
            return False
        if not 0 <= int(ind) < len(self._data):
            return False
        return True


    def get_record(self, ind):
        """Returns record by unique identificator or all records(if ind=='all')"""
        self.load_data()

        if ind == 'all':
            return self._data if self._data else {"Message": "No records."}

        if not self.validate_index(ind):
            return {"Error": "Wrong identificator"}

        ind = int(ind)

        return self._data[ind] if self._data else {"Message": "Record by this identificator is empty"}

    def update_record(self, ind, data):
        """Updades record bu unique identificator, if it exists"""
        if not data:
            return {"Error": "No data for update"}

        self.load_data()

        if not self.validate_index(ind):
            return {"Error": "Wrong identificator"}

        data.pop('time_created', None)
        ind = int(ind)

        if not self._data[ind]:
            print(ind, len(self._data))
            return {"Error": "Cannot update empty record"}

        old_rec = copy.deepcopy(self._data[ind])
        self._data[ind].update(data)
        new_record = copy.deepcopy(self._data[ind])
        self.dump_data()

        return {"Updated": {'old record': old_rec, "new record": new_record}}


    def create_record(self, data):
        """Creates new record"""
        if not all(map(lambda x: x in data.keys(), ('name', 'time_created', 'age'))):
            return {"Error": "Missing one or both of required fields: 'name', 'time_created', 'age'"}

        self.load_data()
        self._data.append(data)
        self.dump_data()

        return {"Record created": data}

    def delete_record(self, ind):
        """Deletes record by identificator or all records(if ind=='all')"""
        self.load_data()

        if ind == 'all':
            self._data = [{} for _ in self._data]
            self.dump_data()
            return {"Message": "All records deleted!"}

        if not self.validate_index(ind):
            return {"Error": "Wrong identificator"}

        ind = int(ind)
        record = copy.deepcopy(self._data[ind])
        self._data[ind] = {}
        self.dump_data()

        return {"Deleted": record} if record else {"Message": "Nothing to delete, record not exists"}
