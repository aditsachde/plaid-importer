from fastapi import BackgroundTasks, FastAPI, Request, status, Header, Response
from pydantic import BaseModel
from typing import Any, List
from verifyPlaidJwt import verify
from updater import updater
from plaidClient import creds

app = FastAPI()

class Webhook(BaseModel):
    webhook_type: str
    webhook_code: str
    item_id: str
    error: Any = None
    new_transactions: int = None
    removed_transactions: List[str] = None

@app.middleware("http")
async def verifyWebhook(request: Request, call_next):
    if not request.headers.get("plaid-verification"):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    if not verify(await request.body(), request.headers['plaid-verification']):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    return await call_next(request)

@app.post("/process-webhook")
async def processWebhook(background_tasks: BackgroundTasks, webhook: Webhook):
    if webhook.webhook_type == "TRANSACTIONS":
        if webhook.webhook_code == "DEFAULT_UPDATE" and webhook.new_transactions != 0:
            background_tasks.add_task(updater, creds.access_token, count=webhook.new_transactions)
    print("reached")
    return {"message": "Processing in the background"}