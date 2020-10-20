import hashlib
import hmac
import time

import requests
from jose import jwt
from plaidClient import plaid_creds

# Plaid client credentials.
CLIENT_ID = plaid_creds.client_id
SECRET = plaid_creds.secret

# Endpoint for getting public verification keys.
ENDPOINT = 'https://'+plaid_creds.environment+'.plaid.com/webhook_verification_key/get'

# Cache for webhook validation keys.
KEY_CACHE = {}


def verify(body, signed_jwt):
   current_key_id = jwt.get_unverified_header(signed_jwt)['kid']

   # If the key is not in the cache, update all non-expired keys.
   if current_key_id not in KEY_CACHE:
       keys_ids_to_update = [key_id for key_id, key in KEY_CACHE.items()
                             if key['expired_at'] is None]
       keys_ids_to_update.append(current_key_id)

       for key_id in keys_ids_to_update:
           r = requests.post(ENDPOINT, json={
               'client_id': CLIENT_ID,
               'secret': SECRET,
               'key_id': key_id
           })

           # If this is the case, the key ID may be invalid.
           if r.status_code != 200:
               continue

           response = r.json()
           key = response['key']
           KEY_CACHE[key_id] = key

   # If the key ID is not in the cache, the key ID may be invalid.
   if current_key_id not in KEY_CACHE:
       return False

   # Fetch the current key from the cache.
   key = KEY_CACHE[current_key_id]

   # Reject expired keys.
   if key['expired_at'] is not None:
       return False

   # Validate the signature and extract the claims.
   try:
       claims = jwt.decode(signed_jwt, key, algorithms=['ES256'])
   except jwt.JWTError:
       return False

   # Ensure that the token is not expired.
   if claims["iat"] < time.time() - 5 * 60:
       return False

   # Compute the has of the body.
   m = hashlib.sha256()
   m.update(body)
   body_hash = m.hexdigest()

   # Ensure that the hash of the body matches the claim.
   # Use constant time comparison to prevent timing attacks.
   return hmac.compare_digest(body_hash, claims['request_body_sha256'])