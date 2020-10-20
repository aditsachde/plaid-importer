#!/usr/bin/env python3
from dbModel import Accounts
from plaidClient import plaid_creds

import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

db = sqlalchemy.create_engine(plaid_creds.database)
Session = sessionmaker(bind=db)
