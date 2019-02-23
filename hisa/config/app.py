from __future__ import absolute_import

class AppConfig(BaseConfig):
    NAME                 = 'hisa'
    VERSION              = (0,1,0)

    ENVIRONMENT_VARIABLE = {
        'alpha_vantage_api_key': 'HISA_ALPHA_VANTAGE_API_KEY',
        'twitter_api_key': 'HISA_TWITTER_API_KEY',
        'twitter_api_secret': 'HISA_TWITTER_API_SECRET',
        'twitter_access_token': 'HISA_TWITTER_ACCESS_TOKEN',
        'twitter_access_token_secret': 'HISA_TWITTER_ACCESS_TOKEN_SECRET'
    }
