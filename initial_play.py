

from api_key import key, url


# connecting
import weaviate
import os

with weaviate.connect_to_wcs(
    cluster_url = url,  
    auth_credentials = weaviate.auth.AuthApiKey(key)  
) as client:  # Use this context manager to ensure the connection is closed
    print(client.is_ready())