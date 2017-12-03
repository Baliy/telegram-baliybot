from flask import Flask
app = Flask('web')

@app.route("/")
def hello():
    print('hello')
    return "<b>Hallo Welt</b>"

app.run(port=80)

