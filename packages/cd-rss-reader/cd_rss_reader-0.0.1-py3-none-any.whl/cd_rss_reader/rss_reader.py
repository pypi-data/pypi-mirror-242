import feedparser


class RSSReader:
    def __init__(self, url):
        self.url = url
        self.feed = None
        self.last_modified = None
        self.etag = None

    def fetch(self):
        """Fetch the RSS feed and store it in the instance."""
        # Using the etag and last_modified values for conditional requests
        parsed_feed = feedparser.parse(self.url, etag=self.etag, modified=self.last_modified)

        # If the status is 304, it means the feed hasn't changed.
        if getattr(parsed_feed, 'status', None) == 304:
            print('The feed has not been modified since last check.')
            return

        # Update the feed only if there are new entries or it is being fetched for the first time
        self.feed = parsed_feed

        if not self.feed.entries:
            raise ValueError("Failed to fetch or parse the RSS feed.")

        # Updating the etag and last_modified values
        self.etag = getattr(self.feed, 'etag', None)
        self.last_modified = getattr(self.feed, 'modified', None)

    def get_entries(self):
        """Return all entries from the fetched feed."""
        if not self.feed:
            self.fetch()
        return self.feed.entries

    def get_title(self):
        """Return the title of the fetched feed."""
        if not self.feed:
            self.fetch()
        return self.feed.feed.title

    def get_link(self):
        """Return the link of the fetched feed."""
        if not self.feed:
            self.fetch()
        return self.feed.feed.link

    def get_feed_description(self):
        """Return the description of the fetched feed."""
        if not self.feed:
            self.fetch()
        return self.feed.feed.description

    def get_image_link(self, entry):
        """Return the image link from an entry, if available."""
        if "media_content" in entry:
            for media in entry.media_content:
                if media.get("type", "").startswith("image/"):
                    return media["url"]
        elif "enclosures" in entry:
            for enclosure in entry.enclosures:
                if enclosure.get("type", "").startswith("image/"):
                    return enclosure["href"]
        return None

