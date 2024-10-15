"""main script"""

import pandas as pd
from my_packages import web_logger

df = web_logger.web_scrape()

print(df)