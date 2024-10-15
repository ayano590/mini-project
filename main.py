"""main script"""

from my_packages import web_logger, api_logger

artists = web_logger.web_scrape()

events = api_logger.api_events()

print(events)