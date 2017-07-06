TOKEN = '433784852:AAEeqexG37bwUs15_2QbO3h2DEQB2E0sRuM'

STATS_URL = "https://abit.ifmo.ru/bachelor/statistics/applications/"
ABIT_LIST_URL = "https://abit.ifmo.ru/bachelor/rating_rank/all/60/"

WEBHOOK_HOST = 'https://ctifmobot.herokuapp.com/'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './cert.pem'
WEBHOOK_SSL_PRIV = './private.key'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % TOKEN
