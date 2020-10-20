from plaidClient import plaidClient
from dbSession import Session
from dbModel import Items, Accounts, Transactions, Balances
from dateutil.relativedelta import relativedelta
import datetime

session = Session()


def updater(access_token, count=500, offset=0, txOnly=False):
    print(access_token, " ", count)
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    start = (datetime.datetime.now() -
             relativedelta(years=2)).strftime("%Y-%m-%d")
    response = plaidClient.Transactions.get(
        access_token, start, end, count=count, offset=offset)

    if not txOnly:
        item(response["item"])
        accounts(response["accounts"], response["item"]["item_id"])
    transactions(response["transactions"])

    session.commit()

    return len(response["transactions"]), response["total_transactions"]


def item(item):
    item_id = item["item_id"]
    exists = session.query(Items).filter_by(item_id=item_id).first()
    if not exists:
        session.add(Items(item_id=item_id, data=item))
    else:
        exists.data = item


def accounts(accounts, item_id):
    time = datetime.datetime.now()
    for account in accounts:
        account_id = account["account_id"]
        exists = session.query(Accounts).filter_by(
            account_id=account_id).first()
        if not exists:
            session.add(Accounts(account_id=account_id,
                                 item_id=item_id, data=account))
        balance = account["balances"]
        session.add(Balances(account_id=account_id, timestamp=time,
                             available=balance["available"], current=balance["current"], 
                             currency=balance["iso_currency_code"], limit=balance["limit"]))


def transactions(transactions):
    for transaction in transactions:
        account_id = transaction["account_id"]
        transaction_id = transaction["transaction_id"]
        exists = session.query(Transactions).filter_by(
            transaction_id=transaction_id).first()
        if not exists:
            session.add(Transactions(account_id=account_id,
                                     transaction_id=transaction_id, data=transaction))
