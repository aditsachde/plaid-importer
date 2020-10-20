from updater import updater
from plaidClient import creds

fetched, total = updater(creds.access_token)
print(fetched, " ", total)

while fetched < total:
    fetched += updater(creds.access_token, offset=fetched, txOnly=True)[0]
    print(fetched, " ", total)