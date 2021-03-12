from flask import Flask, render_template, redirect, request
from jproperties import Properties
from models import Participant, ParticipantSchema
from authlib.integrations.requests_client import OAuth1Session

import config

configs = Properties()
with open('config.properties', 'rb') as config_file:
    configs.load(config_file)

# Get the application instance
connex_app = config.connex_app
# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

app = config.app

alredyRegisterd = "You are alredy registerd to the Portal. Thank you."
doneRegisterd = "Thank you for registering to the project Portal."
testRegisterd = "Test Output Massage."

@app.route('/auth')
def auth():
    print("Auth")
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    print(request.args)
    participant = Participant.query.filter_by(oauth_token=oauth_token).first()
    participant.oauth_verifier = oauth_verifier

    client = OAuth1Session(configs.get("CONSUMER_KEY").data, configs.get("CONSUMER_SECRET").data,
                           token=oauth_token, token_secret=oauth_verifier)
    client.parse_authorization_response(request.url)
    token = client.fetch_access_token(configs.get("FETCH_ACCESS_TOKEN_URL").data, verifier=oauth_verifier)
    participant.user_oauth_token = token['oauth_token']
    participant.user_oauth_token_secret = token['oauth_token_secret']
    config.db.session.commit()
    return render_template('home.html', msg_text=doneRegisterd)

@app.route('/')
def home():
    studyid = request.args.get('studyid')
    participant = Participant.query.filter_by(study_id=studyid).first()
    if participant != None and participant.oauth_verifier != None:
        return render_template('home.html', msg_text=alredyRegisterd)
    client = OAuth1Session(configs.get("CONSUMER_KEY").data, configs.get("CONSUMER_SECRET").data)
    client.redirect_uri = configs.get("REDIRECT_URI").data
    request_token = client.fetch_request_token(configs.get("REQUEST_TOKEN_URL").data)
    authorization_url = client.create_authorization_url(configs.get("AUTHENTICATE_URL").data,
                                                        request_token['oauth_token'])
    if participant == None:
        participant = Participant(study_id=studyid, oauth_token=request_token['oauth_token'],
                                  oauth_token_secret=request_token['oauth_token_secret'],
                                  authorization_redirect_url=authorization_url)
        config.db.session.add(participant)
    else:
        participant.oauth_token = request_token['oauth_token']
        participant.oauth_token_secret = request_token['oauth_token_secret']
        participant.authorization_redirect_url = authorization_url
    config.db.session.commit()
    return redirect(authorization_url, code=302)

@app.route('/testPage')
def testPage():
    return render_template('home.html', msg_text=testRegisterd)

@app.route('/createDB')
def createDB():
    config.db.create_all()
    return render_template('home.html', msg_text='DB Created.')

if __name__ == '__main__':
    app.run(host=configs.get("HOST").data, debug=configs.get("DEBUG").data)
