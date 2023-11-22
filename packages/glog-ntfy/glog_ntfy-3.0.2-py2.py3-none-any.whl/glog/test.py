from notifier import Notifier

config_data = {
    'message': 'test',
    'service': 'ntfy',
    'ntfy_host': 'http://172.25.1.1:8097/fred'
}
logger = Notifier(config_data)
logger.info('[Fred - info] test')