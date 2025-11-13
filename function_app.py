
import logging
import azure.functions as func
import json
import os
from datetime import datetime, timedelta
from azure.eventhub import EventHubProducerClient, EventData
from newsapi import NewsApiClient
from textblob import TextBlob
from blueprint import blueprint

# Read environment variables
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
EVENT_HUB_CONN_STR = os.environ.get("EVENT_HUB_CONN_STR")
EVENT_HUB_NAME = os.environ.get("EVENT_HUB_NAME")

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity if text else 0

app = func.FunctionApp()
@app.function_name(name="timer_trigger")

@app.timer_trigger(
    schedule="0 0 */6 * * *",  # once every 6 hours
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Fetching news...")
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    from_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    articles = newsapi.get_everything(
        q="Artificial Intelligence",
        language="en",
        from_param=from_date,
        sort_by="publishedAt",
        page_size=50
    ).get("articles", [])

    for article in articles:
        article["sentiment"] = get_sentiment(article.get("description", ""))

    logging.info(f"Sending {len(articles)} articles to Event Hub...")
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONN_STR,
        eventhub_name=EVENT_HUB_NAME
    )
    batch = producer.create_batch()
    for article in articles:
        batch.add(EventData(json.dumps(article)))
    producer.send_batch(batch)
    producer.close()
    logging.info("Timer trigger executed successfully.")
    
app.register_functions(blueprint)