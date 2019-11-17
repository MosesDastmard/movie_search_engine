import collector_utils
movies_urls = [collector_utils.get_urls(i) for i in range(1,3)]
#%%
movies_urls[0].update(movies_urls[1])
movies_urls = movies_urls[0].copy()
collector_utils.scraping(movies_urls, 1)
