from tinydb import TinyDB, Query

db = TinyDB('./db.json')

Eintrag = Query()
einträge = db.all()

user_einträge = dict()
for e in einträge:
    liste = user_einträge.setdefault(e['user'], [])
    liste.append(e)

for user, einträge in user_einträge.items():
    print(user)
    for e in einträge:
        print("    %s %s" % (e['date'], e['command']))
