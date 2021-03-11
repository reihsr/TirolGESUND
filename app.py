from flask import Flask, render_template
from jproperties import Properties
import connexion

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)

app = connexion.App(__name__, template_folder="templates", specification_dir='./')
app.add_api('swagger.yml')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host=configs.get("HOST").data, debug=configs.get("DEBUG").data)
