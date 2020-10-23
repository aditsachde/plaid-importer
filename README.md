# Plaid Transaction Importer

This is a very WIP set of scripts and stuff to fetch transactions from Plaid and put them in a database.

## Goals
- Import transactions from Plaid into a postgresql database.
- Listen to webhooks for ongoing transaction data.
- Store balance over time.
- Support listening to multiple accounts
- Support storing credentials in a database, instead of a config file.

### Why?
Having transactions stored in a database and continuously updated makes it simple to use this for other purposes later on.

For example, using Grafana to plot the balance table or listening for new rows on the transactions database and triggering notifications.

## Usage

### Create a virtual environment
Create a new virtual environment using `python3 -m venv venv` 
Activate the virtual environment using `source venv/bin/activate`
Install the requirements using `pip install -r requirements.txt`

### Authenticating and other required information
Authenticate with Plaid using `python authenticateAccount.py`. This will open a webpage where you can authenticate with Plaid. Once authenticated, the plaid public token will be exchanged for an access token. The access token and item id will be stored in a `credentials.yaml`.

You will also need to add a webhook url, a database url, and the Plaid credentials. Look at the config section for more information.

### Database setup
This repo uses alembic to perform database migrations. Alembic should have already been installed as part of the requirements. If you have filled in the database url in your config file, you can simply do `alembic upgrade head` to apply all the necessary changes. Use a fresh database.

#### Compatability
Right now, only postgresql is tested, and is likely the only database that will work, as I use the JSONB column type from postgres to store data, instead of properly creating columns for every single field Plaid returns when querying for items, accounts, and transactions. 

### Historical Transaction Import
Use `python historicalUpdate.py` to import all previous transactions into the database.

### Webhook support
TODO

## Config
```
accessToken: access token, autofilled

itemId: item id, autofilled

webhook: webhook url, this is used to initialize Link and CANNOT BE EMPTY.
    Must be a valid url, including "https://". Use something like https://example.com if you don't care about webhooks.

database: Database connection url
    postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]

clientId: Plaid client ID

secret: Plaid environment secret

environment: Plaid environment, sandbox or development
```