import pymongo
import copy

class SubDocument:

    def __init__(self, document, setPath):
        self._document = document
        self._setPath = setPath

    def set(self, value):
        self._document._collection.update_one(
            self._document._query,
            {"$set" : {self._setPath : value}}
        )

    def __getitem__(self, key):
        if isinstance(key, str):
            setPath = self._setPath + "." + key
        elif isinstance(key, int):
            setPath = self._setPath + "." + str(key)

        return SubDocument(
            self._document,
            setPath
        )
    
    def __setitem__(self, key, value):
        self[key].set(value)

    def append(self, value):
        self._document._collection.update_one(
            self._document._query,
            {"$push" : {self._setPath : value}}
        )

    def get(self):

        parts = self._setPath.split('.')
        for i in range(len(parts)):
            if parts[i].isnumeric():
                projection = ".".join(parts[:i])
                break
        else:
            projection = self._setPath

        value = self._document._collection.find_one(
            filter = self._document._query,
            projection = {projection : 1}
        )

        for part in parts:
            if part.isnumeric():
                index = int(part)
                value = value[index]
            else:
                value = value[part]
        
        return value

    def drop(self):
        self._document._collection.update_one(
            self._document._query,
            {"$unset" : {self._setPath : 1}}
        )

    def __contains__(self, key):
        query = copy.deepcopy(self._document._query)
        query[self._setPath + "." + key] = {"$exists" : True, "$ne" : None}

        return self._document._collection.find_one(filter = query) is not None

class Document:

    def __init__(self, collection, query, _id = None):
        self._collection = collection
        self._query = query
        self._id = _id

    def set(self, key, value):
        self._collection.update_one(self._query, {"$set" : {key : value}})
    
    def get(self):
        return self._collection.find_one(self._query)
    
    def __getitem__(self, key):
        return SubDocument(self, key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def getId(self):
        if self._id is not None:
            return self._id
        
        self._id = self['_id'].get()
        return self._id

    def drop(self):
        self._collection.delete_one(filter = self._query)

    def __contains__(self, key):
        query = copy.deepcopy(self._query)
        query[key] = {"$exists" : True, "$ne" : None}

        return self._collection.find_one(filter = query) is not None

class Collection:
    
    def __init__(self, collection):
        self._collection = collection
        self.raw = collection

    def byId(self, _id):
        query = {"_id" : _id}
        return Document(collection = self._collection, query = query, _id = _id)

    def new(self, value = None):
        if value is None:
            value = {}

        _id = self._collection.insert_one(value).inserted_id
        query = {"_id" : _id}
        return Document(collection = self._collection, query = query)

    def first(self):
        query = {}
        return Document(collection = self._collection, query = query)

    def where(self, key, value):
        query = {key : value}
        return Document(collection = self._collection, query = query)

    def drop(self):
        self._collection.drop()

class Database:

    def __init__(self, host, name):
        self.name = name
        self._client = pymongo.MongoClient(host)
        self._db = self._client[name]
        self.raw = self._db

    def collection(self, collectionName):
        return Collection(collection = self._db[collectionName])
    
    def __getitem__(self, collectionName):
        return Collection(collection = self._db[collectionName])
    
    def drop(self):
        self._client.drop_database(self.name)

db = Database(host = "mongodb://localhost:27017/", name = "bia")
