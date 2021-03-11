from flask import Flask, render_template
from jproperties import Properties

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)

app = Flask(__name__, template_folder="templates")


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host=configs.get("HOST").data, debug=configs.get("DEBUG").data)
