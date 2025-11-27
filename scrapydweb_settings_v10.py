"""ScrapydWeb settings file.

Automatically loaded by `scrapydweb` if placed in the working directory.
Adjust values as needed; restart ScrapydWeb after changes.
"""

# List of Scrapyd server base URLs (must end with / if using trailing slash semantics)
SCRAPYD_SERVERS = [
    'http://0.0.0.0:8800',
]

# Default server where new actions apply if not specified
SCRAPYD_DEFAULT = 'http://0.0.0.0:8800'

# Timezone for UI display (use tz database names, e.g. 'UTC', 'Asia/Shanghai')
TIMEZONE = 'UTC'

# Authentication (disabled by default for local use). Set ENABLE_AUTH=True and provide creds if exposed externally.
ENABLE_AUTH = False
AUTH_USERNAME = 'admin'
AUTH_PASSWORD = 'change_me'  # Change when enabling auth

# Retention options (tweak to control cleanup behavior)
MAX_JOB_LOGS = 200  # Max number of job logs retained per spider

# Toggle debug for verbose internal logging
DEBUG = False

# Example advanced options (uncomment to use):
# REQUESTS_TRUST_ENV = True  # Honor system proxies, etc.
# RUN_SCRAPYD_ON_START = False  # If True, ScrapydWeb attempts to launch scrapyd automatically

# Notes:
# - Run `scrapyd` in a separate terminal before starting ScrapydWeb.
# - Deploy: `scrapyd-deploy default -p basic_spider`
# - Schedule via UI or: curl http://0.0.0.0:8800/schedule.json -d project=basic_spider -d spider=quotes
