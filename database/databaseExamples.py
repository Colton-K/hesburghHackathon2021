
# probably best to import this way
from database.database import db

# The top level of a database contains collections; use this to get one (it
# will be autocreated if it doesn't exist yet)

cpus = db.collection('cpus')

# Each collection contains documents which are essentially json files. Use the
# new method to add a new document to a collection

myCpu = cpus.new({
    'model' : 'i7-6700hq',
    'arch' : 'x86',
    'cores' : 4,
    'threads' : 8,
    'base_clock' : 2.6,
    'cache' : {
        'l1d' : 128,
        'l1i' : 128,
        'l2' : 1024,
    },
    'flags' : ['fpu', 'sse', 'sse2']
})

# the return value is essentially a python handle for the document that was
# created. Some functions you can do with it are:
#   get()       return the contents
#   getId()     get the unique '_id' field MongoDB generate for each document

print(myCpu.get())
print(myCpu.getId())

# Like python json manipulation, you can use square brackets to get dictionary
# keys and list indexes; the following methods are availble for read/modify
#   get()           gets contents
#   set(<value>)    set a new value; will create if key doesn't exist
#   append(<value>) append to back of array (won't work on dictionary)

print( myCpu['arch'].get()          )
print( myCpu['cache']['l1i'].get()  )
print( myCpu['flags'][1].get()      )

myCpu['arch'].set('x86-64')
myCpu['boost_clock'].set(3.5)
myCpu['cache']['l3'] = 6144     # assignment like this is equivalent to .set()
myCpu['flags'].append('aes')

print(myCpu.get())

# To retrieve a document later, there are a couple of options:
#   collection.byID(<id>)           if you know the documents unique '_id'
#   collection.first()              get the first document in the collection
#   collection.where(key, value)    get first document with key-value pair

sameCpu1 = cpus.byId(myCpu.getId())
sameCpu2 = cpus.first()
sameCpu3 = cpus.where('model', 'i7-6700hq')

# Individual subfields, documents, and entire collections can be removed with
# the drop method:

myCpu['threads'].drop()
myCpu['cache']['l1i'].drop()
myCpu['flags'].drop()

print(myCpu.get())

myCpu.drop()        # delete document
cpus.drop()         # delete whole collection
