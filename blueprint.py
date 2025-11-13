
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
import json
from datetime import datetime

blueprint = func.Blueprint()
@blueprint.function_name(name="eventhub_to_blob")
@blueprint.event_hub_message_trigger(arg_name="azeventhub",event_hub_name="EVENT_HUB", connection="EVENT_HUB_CONN_STR" )
def eventhub_to_blob(azeventhub: func.EventHubEvent):
    BLOB_CONN_STR = os.environ.get("BLOB_CONN_STR")
    CONTAINER = os.environ.get("NEWS_CONTAINER_NAME")

    if not BLOB_CONN_STR or not CONTAINER:
        logging.error("Missing Blob Storage environment variables")
        return

    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    container_client = blob_service_client.get_container_client(CONTAINER)
    try:
        container_client.create_container()
    except Exception:
        pass

    data = json.loads(azeventhub.get_body().decode('utf-8'))
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    blob_name = f"news_{timestamp}.json"

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(data), overwrite=True)
    logging.info(f"Stored event in Blob: {blob_name}")
