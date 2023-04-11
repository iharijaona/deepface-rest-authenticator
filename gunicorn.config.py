from deepface_rest import Config

bind = f'0.0.0.0:{Config.APP_PORT}'

workers = 5
# worker_class = 'gevent'

accesslog = '-'

timeout = 300
