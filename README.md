# Azure-News-Sentiment-Pipeline

The Azure News Sentiment Pipeline is a serverless data pipeline built with **Azure Functions (Python)** that automatically:
1. Fetches the latest Subject: **Artificial Intelligence (AI)** news from the **NewsAPI** every few hours.
2. Performs **sentiment analysis** on each news article using **TextBlob**.
3. Streams the processed articles to **Azure Event Hub**.
4. Stores the results as **JSON files in Azure Blob Storage** for analysis or reporting.

Features

**Automated News Fetching** — runs on a 6-hour interval using Azure Timer Trigger.  
**Sentiment Analysis** — classifies articles as positive, neutral, or negative using TextBlob.  
**Event Streaming** — streams processed data to Azure Event Hub for scalability.  
**Blob Storage Archival** — saves each article batch as a JSON file in Azure Blob Storage.  
**Serverless Deployment** — runs entirely on Azure Functions (no manual servers or cron jobs).  


### Working:
### 1. Timer Trigger (Data Fetching & Processing)
- Runs automatically every 6 hours (`0 0 */6 * * *`).
- Fetches latest AI news articles using **NewsAPI**.
- Performs **sentiment analysis** using **TextBlob**.
- Sends the processed JSON articles to **Azure Event Hub**.

### 2. Event Hub Trigger (Data Storage)
- Listens for incoming messages from **Event Hub**.
- Converts each message into JSON.
- Saves it in **Azure Blob Storage** with a timestamped filename.

## Environment Variables

Add these in **Azure Function App → Configuration → Application Settings**:

| Variable | Description |
|-----------|-------------|
| `NEWS_API_KEY` | API key from [NewsAPI.org](https://newsapi.org) |
| `EVENT_HUB_CONN_STR` | Event Hub connection string |
| `EVENT_HUB_NAME` | Event Hub name (e.g. `news_eh`) |
| `BLOB_CONN_STR` | Azure Blob Storage connection string |
| `NEWS_CONTAINER_NAME` | Blob container name (e.g. `newsdata`) |
| `FUNCTIONS_WORKER_RUNTIME` | Set to `python` |


## requirements.txt

```txt
azure-functions
azure-eventhub
azure-storage-blob
newsapi-python
textblob
