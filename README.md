#  URL Shortener API

A backend URL shortener service built with FastAPI, PostgreSQL, SQLAlchemy, and Redis.  
It converts long URLs into short, shareable links and redirects users quickly using caching for performance.


##  Features

- Shorten long URLs into unique short codes
- Fast redirection to original URLs
- Redis caching for high-speed redirects
- PostgreSQL database storage
- URL expiration support
- Duplicate URL handling (prevents creating multiple short codes for the same original URL; returns existing short code if URL already exists)
- Input validation using Pydantic
- RESTful API structure


## How It Works

1. User submits a long URL
2. System generates a unique short code
3. URL mapping is stored in PostgreSQL
4. Short code is cached in Redis for fast lookup
5. When accessed, user is redirected to the original URL


## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Redis (Caching)
- Pydantic (Validation)
- Uvicorn
- Python-dotenv


##  Project Structure
#  URL Shortener API

A backend URL shortener service built with FastAPI, PostgreSQL, SQLAlchemy, and Redis.  
It converts long URLs into short, shareable links and redirects users quickly using caching for performance.


## Features

- Shorten long URLs into unique short codes
- Fast redirection to original URLs
- Redis caching for high-speed redirects
- PostgreSQL database storage
- URL expiration support
- Duplicate URL handling (reuses existing short links)
- Input validation using Pydantic
- RESTful API structure


## How It Works

1. User submits a long URL
2. System generates a unique short code
3. URL mapping is stored in PostgreSQL
4. Short code is cached in Redis for fast lookup
5. When accessed, user is redirected to the original URL


## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Redis (Caching)
- Pydantic (Validation)
- Uvicorn
- Python-dotenv



## Project Structure

```
app/
├── main.py
├── db/
│ └── database.py
├── models/
│ └── model.py
├── routes/
│ └── url_route.py
├── services/
│ └── url_service.py
├── schemas/
│ └── url.py
├── core/
│ └── redis.py
alembic/
.env
requirements.txt
```

## API Endpoints

### Create Short URL

**POST** `/url/shorten`

#### Request Body

```json
{
  "original_url": "https://example.com"
}
Response
{
  "short_url": {
    "short_url": "your_domaiain/abc123",
    "original_url": "https://example.com"
  }
}
```
### Redirect to Original URL

**GET** `/url/{short_code}`

*Behavior*
- Checks Redis cache first
- Falls back to PostgreSQL if not found
- Redirects user to original URL

### System Design Overview
**Caching (Redis)**
- Stores: short_code → original_url
- Speeds up redirects
- Reduces database load
**Database (PostgreSQL)**
*Stores:*
- original URL
- short code
- timestamps
- expiration time (optional)
**Expiry System**
- Links can expire after a set time
- Expired links return an error response
**Duplicate Handling**
*If a URL already exists:*
- system returns existing short code instead of creating a new one

### Example Usage
**Create short URL**
```
curl -X POST "http://127.0.0.1:8000/url/shorten" \
-H "Content-Type: application/json" \
-d '{"original_url": "https://example.com"}'
Open short URL
http://127.0.0.1:8000/url/abc123
```
### Validation & Security
- URL validation using Pydantic (HttpUrl)
- Protection against invalid input
- Future improvements:
- rate limiting
- blocked domains
- authentication layer


1. Clone repository
```bash
git clone https://github.com/yourusername/url-shortener.git
```
cd url-shortener

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Setup environment variables

Create .env file:
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/url_shortener
SECRET_KEY=your_secret_key

5. Run migrations
```bash
alembic upgrade head
``` 

6. Start server
```bash
uvicorn app.main:app --reload
```