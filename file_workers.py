import json
from collections import defaultdict
import copy


class FileReaderAndWriter:
    def __init__(self, path: str):
        self.path = path
        self.data = None

    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data = f.read()

    def write(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(self.data)


class JsonLinesConverter(FileReaderAndWriter):
    def json_to_dict(self):
        self.data = [json.loads(line) for line in self.data.split('\n')] if self.data else self.data

    def dict_to_json(self):
        self.data = '\n'.join([json.dumps(line) for line in self.data])


class DatabaseImitation(JsonLinesConverter):
    def create_db(self):
        self.db = defaultdict(list)
        for record in self.data:
            self.db[record['name']+str(record['time_created'])] += [record]

    def load_data(self):
        self.read()
        self.json_to_dict()
        self.create_db()

    def dump_data(self):
        self.data = [record for v in self.db.values() for record in v]
        self.dict_to_json()
        self.write()


class DataWorker(DatabaseImitation):
    def get_record(self, ind):
        self.load_data()

        if ind == 'all':
            if not self.data:
                return {"Message": "No records."}
            return self.data

        return self.db[ind] if self.db[ind] else {"message": "Record not found"}

    def update_record(self, ind, data):
        self.load_data()

        if ind not in self.db:
            return {"Error": "Record not found"}

        data.pop('name', None)
        data.pop('time_created', None)
        old_rec = copy.deepcopy(self.db[ind])
        for rec in self.db[ind]:
            rec.update(data)
        self.dump_data()

        return {"Updated": {'old record': old_rec, "new record": self.db[ind]}}

    def create_record(self, data):
        self.load_data()
        if 'name' not in data.keys() or 'time_created' not in data.keys():
            return {"Error": "Missing one or both of required fields: 'name', 'time_created'"}

        record_id = data['name'] + str(data['time_created'])

        if record_id in self.db.keys():
            return {"Error": "Record already exists"}

        self.db[record_id] = [data]
        self.dump_data()

        return {"Record created": data}

    def delete_record(self, ind):
        if ind == 'all':
            self.db = {}
            self.dump_data()
            return {"Message": "All records deleted!"}

        self.load_data()
        record = self.db[ind][:]
        del self.db[ind]
        self.dump_data()

        return {"Deleted": record} if record else {"Message": "Nothing to delete, record not exists"}








