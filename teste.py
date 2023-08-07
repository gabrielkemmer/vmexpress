from pymongo import MongoClient

# Replace the connection string and database name with your MongoDB details
client = MongoClient('mongodb+srv://gabrielkemmer:Fn741953.741953@microblog.ojr4lzw.mongodb.net/?retryWrites=true&w=majority')
db = client['guilherme']
users_collection = db['users']
consults_collection = db['consultas']
cnpj = '18398145000158'

# Query to find all documents with "cnpj" field equal to the provided cnpj
query = {"CNPJ": cnpj}

# Fetch all matching documents
cursor = consults_collection.find(query)

# Convert the cursor to a list of documents
result = list(cursor)

# Close the MongoDB connection
client.close()

print(result)
