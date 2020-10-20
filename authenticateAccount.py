from uuid import uuid4
from plaidClient import plaidClient, plaid_creds
from flask import Flask, render_template, request
import logging
import json
import webbrowser
import os
import signal
import sys
import yaml

############# CLEANLY HANDLE CTRL-C #############

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

############# GET LINK TOKEN #############

link_token_response = plaidClient.LinkToken.create(configs={
    'user': {
      'client_user_id': uuid4().hex,
    },
    'products': ["transactions"],
    'client_name': "Transactions.fyi",
    'country_codes': ['US'],
    'language': 'en',
    'webhook': plaid_creds.webhook,
  })

link_token = link_token_response["link_token"]

############# AUTHENTICATE USER #############

public_token = ""

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
#os.environ['WERKZEUG_RUN_MAIN'] = 'true'

@app.route('/')
def authenticate():
  return render_template('authenticate.html', link_token=link_token)

@app.route('/publicToken', methods=['POST'])
def publicTokenExchange():
  data = request.form
  global public_token 
  public_token = data["public_token"]
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
  func()
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

print("Authenticate in your browser, then come back!")
print("If a window does not open, visit http://localhost:5000")
print("In some cases, you may have to reload the page")
print()
webbrowser.open('http://localhost:5000')
app.run()
print()

############# EXCHANGE PUBLIC TOKEN #############

response = plaidClient.Item.public_token.exchange(public_token)

access_token = response["access_token"]
item_id = response["item_id"]

credentials = { "accessToken": access_token, "itemId": item_id }

with open("credentials.yaml", 'w') as file:
  documents = yaml.dump(credentials, file)