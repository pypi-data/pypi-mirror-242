# pickpock

This is a slightly cleaned up re-implementation of Deen Freelon's pyktok library for scraping TikTok metadata

I've removed heavy dependencies (numpy, pandas), modernized cookie handling (with request sessions) and modularized the code.

To scrape TikTok metadata, first provide a firefox or chrome cookie database and use the generic dispatch functions:

```python
import pickpock 

# the library always returns generators
results = pickpock.fetch("<some_url>")
# there are two convenience functions for writing either raw metadata as jsonlines
for video in pickpock.fetch("<some_url>"):
    pickpock.write_json(video)
# or to write a csv similar to the original pyktok
for video in pickpock.fetch("<some_url>"):
    pickpock.write_csv(video)
```