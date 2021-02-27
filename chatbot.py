from chatterbot import ChatBot
import chatterbot, json
from chatterbot.response_selection import get_first_response, get_most_frequent_response
from chatterbot.comparisons import levenshtein_distance

server, name, db='','',''

with open("config.json") as f:
    data = json.loads(f.read())
    server = data["server_uri"]
    name = data["name"]
    db = data["dbname"]
print(name+' '+db+'\nConnecting to '+server+'...')
pio = ChatBot( #local sql version in comments
    name,
    storage_adapter = "chatterbot.storage.MongoDatabaseAdapter", #"chatterbot.storage.SQLStorageAdapter",
    database = db, #"./db.sqlite3",
    database_uri = server, ##nothing
    input_adapter = "chatterbot.input.VariableInputTypeAdapter",
    output_adapter = "chatterbot.output.OutputAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            
        }
    ],
    statement_comparison_function = chatterbot.comparisons.levenshtein_distance,
    response_selection_method = get_first_response
)
