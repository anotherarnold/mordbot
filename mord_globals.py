import sys, os, json

#A file to hold and juggle global variables

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    application_path = os.path.dirname(__file__)  

def initialize():
    global added_commands
    global list_forbidden
    global react_role
    global role_mess
    global excluded_channels
    global bot_chatter_excluded
    try:
        json_commands = open(application_path + '//data/added_commands.json', 'r')
        added_commands = json.load(json_commands)
        json_commands.close()
    except(FileNotFoundError):
        if os.path.exists(application_path + "//data/") == False:
            os.mkdir(application_path + "//data/")
        json_commands = open(application_path + '//data/added_commands.json', 'w')
        added_commands = {}
        json_commands.write(json.dumps(added_commands))
        json_commands.close()
        
    try:
        json_role = open(application_path + '//data/react_role.json', 'r')
        react_role = json.load(json_role)
        json_role.close()
    except(FileNotFoundError):
        if os.path.exists(application_path + "//data/") == False:
            os.mkdir(application_path + "//data/")
        json_role = open(application_path + '//data/react_role.json', 'w')
        react_role = {"1":{"duck": "\ud83e\udd86"}}
        json_role.write(json.dumps(react_role))
        json_role.close()

    try:
        json_role_mess = open(application_path + '//data/role_mess.json', 'r')
        role_mess = json.load(json_role_mess)
        json_role_mess.close()
    except(FileNotFoundError):
        if os.path.exists(application_path + "//data/") == False:
            os.mkdir(application_path + "//data/")
        json_role_mess = open(application_path + '//data/role_mess.json', 'w')
        role_mess = {}
        json_role_mess.write(json.dumps(role_mess))
        json_role_mess.close()

    try:
        json_excluded = open(application_path + '//data/excluded_channels.json', 'r')
        excluded_list = json.load(json_excluded)
        excluded_channels = set(excluded_list)
        json_excluded.close()
    except(FileNotFoundError):
        if os.path.exists(application_path + "//data/") == False:
            os.mkdir(application_path + "//data/")
        json_excluded = open(application_path + '//data/excluded_channels.json', 'w')
        excluded_channels = set()
        json_excluded.write(json.dumps(list(excluded_channels)))
        json_excluded.close()
    
    try:
        json_bot_chatter_excluded = open(application_path + '//data/bot_chatter_excluded.json', 'r')
        bot_chatter_excluded_list = json.load(json_bot_chatter_excluded)
        bot_chatter_excluded = set(bot_chatter_excluded_list)
        json_bot_chatter_excluded.close()
    except(FileNotFoundError):
        if os.path.exists(application_path + "//data/") == False:
            os.mkdir(application_path + "//data/")
        json_bot_chatter_excluded = open(application_path + '//data/bot_chatter_excluded.json', 'w')
        bot_chatter_excluded = set()
        json_bot_chatter_excluded.write(json.dumps(list(bot_chatter_excluded)))
        json_bot_chatter_excluded.close()


def excluded(ctx):
    return ctx.message.channel.id not in excluded_channels

def save_commands(new_commands):
    global added_commands    
    added_commands = new_commands
    json_commands = open(application_path + '//data/added_commands.json', 'w')
    json_commands.write(json.dumps(added_commands))
    json_commands.close()

def save_roles(new_roles):
    global react_role
    react_role = new_roles
    json_role = open(application_path + '//data/react_role.json', 'w')
    json_role.write(json.dumps(react_role))
    json_role.close()

def save_role_mess(new_role_mess):
    global role_mess
    role_mess = new_role_mess
    json_role_mess = open(application_path + '//data/role_mess.json', 'w')
    json_role_mess.write(json.dumps(role_mess))
    json_role_mess.close()

def save_excluded(new_excluded):
    global excluded_channels
    json_excluded = open(application_path + '//data/excluded_channels.json', 'w')    
    json_excluded.write(json.dumps(list(new_excluded)))
    excluded_channels = new_excluded
    json_excluded.close()

def save_bot_chatter_excluded(new_bot_chatter):
    global bot_chatter_excluded
    json_bot_chatter_excluded = open(application_path + '//data/bot_chatter_excluded.json', 'w')   
    json_bot_chatter_excluded.write(json.dumps(list(new_bot_chatter)))
    bot_chatter_excluded = new_bot_chatter
    json_bot_chatter_excluded.close()

def refresh():
    global added_commands 
    global list_forbidden
    global react_role
    global role_mess
    global excluded_channels     
    global bot_chatter_excluded   
    json_commands = open(application_path + '//data/added_commands.json', 'r')
    added_commands = json.load(json_commands)
    json_commands.close()
    json_role = open(application_path + '//data/react_role.json', 'r')
    react_role = json.load(json_role)
    json_role.close()
    json_role_mess = open(application_path + '//data/role_mess.json', 'r')
    role_mess = json.load(json_role_mess)
    json_role_mess.close()
    json_excluded = open(application_path + '//data/excluded_channels.json', 'r')
    excluded_list = json.load(json_excluded)
    excluded_channels = set(excluded_list)
    json_excluded.close()
    json_bot_chatter_excluded = open(application_path + '//data/bot_chatter_excluded.json', 'r')
    bot_chatter_excluded_list = json.load(json_bot_chatter_excluded)
    bot_chatter_excluded = set(bot_chatter_excluded_list)
    json_bot_chatter_excluded.close()
    
def deletemarkovfile(filename):
    if os.path.exists(application_path + '//data/corpus/' + filename):
        os.remove(application_path + '//data/corpus/' + filename)