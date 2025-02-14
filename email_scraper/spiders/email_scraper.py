import scrapy
import re

class EmailSpider(scrapy.Spider):
    name = "email_scraper"

    def start_requests(self):
        # Read URLs from a text file
        try:
            with open("urls.txt", "r", encoding="utf-8") as file:
                self.urls = [url.strip() for url in file.readlines() if url.strip()]
        except FileNotFoundError:
            self.log("❌ Error: urls.txt file not found!")
            return

        self.processed_count = 0  # Track processed URLs

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract emails using regex
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text))
        
        # Save emails to a file
        with open("emails.txt", "a") as f:
            for email in emails:
                f.write(f"{email}\n")

        self.processed_count += 1  # Increment processed count

        # Check if all URLs have been processed
        if self.processed_count == len(self.urls):
            self.log("\n✅ Done searching!\n")

        yield {"url": response.url, "emails": list(emails)}
