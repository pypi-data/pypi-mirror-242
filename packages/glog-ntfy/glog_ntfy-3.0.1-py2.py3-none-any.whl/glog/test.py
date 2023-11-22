import glog

config_data = {
    'send_to_ntfy': True,
    'service': 'ntfy',
    'ntfy_host': 'http://172.25.1.1:8097/fred'
}
logger = glog.GLog('test', config_data)
logger.info('test')