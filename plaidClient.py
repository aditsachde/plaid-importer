from plaid import Client
import yaml
from dotmap import DotMap

with open("credentials.yaml") as file:
    c = DotMap(yaml.full_load(file))
    creds = DotMap(access_token=c["accessToken"],
                   item_id=c["itemId"])
    plaid_creds = DotMap(client_id=c["clientId"], secret=c["secret"],
                         environment=c["environment"], webhook=c["webhook"], database=c["database"])
    # Access using creds.access_token and creds.item_id

plaidClient = Client(plaid_creds.client_id,
                     plaid_creds.secret, plaid_creds.environment)
