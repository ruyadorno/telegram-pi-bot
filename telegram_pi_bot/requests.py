import ssl
from json import dumps, loads, JSONDecodeError
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

def _get_parsed_data(logger, req_data, msg):
    parsed_data = None
    post_data = req_data.get('data', None)
    message = msg.message.text.replace('/' + req_data.get('command_name'), '')

    if post_data != None:
        if (req_data.get('headers').get('Content-Type') == 'application/json'):
            for key, val in post_data.items():
                post_data[key] = val % message
            parsed_data = dumps(post_data)
        else:
            try:
                parsed_data = post_data % message
            except ValueError as e:
                logger.warn(
                    'Failed to parse string, try to escape it:' +
                    'http://stackoverflow.com/q/8856523/151243'
                )
                parsed_data = post_data
            except TypeError:
                logger.warn('Could not format post data')
                parsed_data = post_data
        parsed_data = parsed_data.encode('utf8')

    logger.debug(parsed_data)

    return parsed_data


def post_json(logger, req_data, msg):
    parsed_data = _get_parsed_data(logger, req_data, msg)
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    try:
        req = Request(
            url=req_data['url'],
            data=parsed_data,
            headers=req_data.get('headers', {}),
            method=req_data.get('method', 'GET')
        )
    except KeyError as e:
        logger.error('A webhook must have a url property')

    try:
        http_res = urlopen(req, context=gcontext)
        res = http_res.read()
        try:
            parsed_res = loads(res.decode())
            logger.debug(parsed_res)
        except JSONDecodeError as e:
            logger.error(e)
            parsed_res = { 'response': res }
    except HTTPError as e:
        logger.error(e)
        parsed_res = {}
    except URLError as e:
        logger.error('Address could not be reached')
        parsed_res = {}

    return parsed_res

