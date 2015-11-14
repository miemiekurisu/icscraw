# Scrapy settings for wayfaircraw project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'wayfaircraw'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['wayfaircraw.spiders']
NEWSPIDER_MODULE = 'wayfaircraw.spiders'
USER_AGENT = '%s' % ('Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6')
DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = True
COOKIES_ENABLES=False
