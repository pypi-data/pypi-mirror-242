# RSSReader

A robust Python-based RSS feed reader that fetches, parses, and manages updates for RSS and Atom feeds. It supports efficient conditional GET requests to minimize bandwidth and server load by utilizing `Last-Modified` and `Etag` HTTP headers.

## Features

- Parses different RSS and Atom feed formats.
- Extracts key details such as titles, links, descriptions, and associated images.
- Utilizes `Last-Modified` and `Etag` headers to perform conditional GET requests, avoiding unnecessary data transfer if the feed has not been updated since the last fetch.

## Requirements

- Python 3
- `feedparser` library

## Installation

First, ensure that you have Python installed on your machine. Then, you can install the required `feedparser` library using `pip`:

```bash
pip install cd-rss-reader
```

Usage
To use the RSSReader class, create an instance with the URL of the RSS feed you wish to parse:

```python

from cd_rss_reader import RSSReader

# Initialize the reader with the feed URL
url = "https://www.example.com/rss_feed_url.xml"
reader = RSSReader(url)

# Fetch and parse the feed
reader.fetch()

# Get basic information about the feed
print(f"Feed Title: {reader.get_title()}")
print(f"Feed Link: {reader.get_link()}")
print(f"Feed Description: {reader.get_feed_description()}")

# Iterate over the feed entries
for entry in reader.get_entries():
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published Date: {entry.published}")
    print(f"Summary: {entry.summary}")
    image_link = reader.get_image_link(entry)
    if image_link:
        print(f"Image Link: {image_link}")
    else:
        print("No image available.")
Replace https://www.example.com/rss_feed_url.xml with the URL of the RSS feed you want to read.
```

Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

More documentation at:
[Code Docta](https://codedocta.com "Code Docta")

License
This project is open-sourced software licensed under the MIT license.