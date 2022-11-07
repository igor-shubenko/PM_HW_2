import json
# if empty file

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


class JsonLinesConverter:
    def json_to_dict(self):
        self.data = [json.loads(line) for line in self.data.split('\n')]

    def dict_to_json(self):
        self.data = '\n'.join([json.dumps(line) for line in self.data])


class JsonFileWorker(FileReaderAndWriter,
                     JsonLinesConverter):
    def __init__(self, path):
        super().__init__(path)
        self.read()
        self.json_to_dict()

    def get_record(self, ind):
        pass

    def update_record(self, ind, data):
        pass

    def create_record(self, data):
        pass

    def delete_record(self, ind):
        pass








