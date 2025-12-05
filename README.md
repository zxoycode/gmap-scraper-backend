# Google Maps Review Scraper Backend (FastAPI + Oxylabs)

This backend provides a simple API to scrape Google Maps reviews using the Oxylabs Web Scraper API.

## API Endpoint

### GET /scrape

Example:

https://YOUR_RENDER_URL.onrender.com/scrape?url=https://maps.app.goo.gl/iBAPEHqmRsbe1BCC7&limit=20


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| url | string | Yes | Google Maps URL (supports short links) |
| limit | int | No | Max number of reviews to fetch (default 150) |

## Environment Variables (Required)

Set these in Render → Environment:

OX_USERNAME=your_oxylabs_username
OX_PASSWORD=your_oxylabs_password


## Deployment (Render)

1. Create new Web Service  
2. Select your GitHub repo  
3. Render auto-detects Python (no Dockerfile needed)  
4. Set environment variables  
5. Deploy!
