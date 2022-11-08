import json
from collections import defaultdict


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
            return self.data
        return self.db[ind] if self.db[ind] else {"message": "Record not found"}

    def update_record(self, ind, data):
        self.load_data()
        pass

    def create_record(self, data):
        pass

    def delete_record(self, ind):
        if ind == 'all':
            self.db = {}
            self.dump_data()
            return {"message": "All records deleted!"}

        self.load_data()
        record = self.db[ind][:]
        del self.db[ind]
        self.dump_data()
        return {"deleted": record} if record else {"message": "Nothing to delete, record not exists"}








