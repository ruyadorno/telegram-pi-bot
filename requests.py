from json import dumps, loads, JSONDecodeError
from urllib.request import urlopen, Request
from urllib.error import HTTPError

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
            parsed_data = post_data % message
        parsed_data = parsed_data.encode('utf8')

    logger.debug(parsed_data)

    return parsed_data


def post_json(logger, req_data, msg):
    parsed_data = _get_parsed_data(logger, req_data, msg)

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
        http_res = urlopen(req)
        res = http_res.read()
        try:
            parsed_res = loads(res.decode())
            logger.debug(parsed_res)
        except JSONDecodeError as e:
            logger.error(e)
            parsed_res = res
    except HTTPError as e:
        logger.error(e)
        parsed_res = {}

    return parsed_res

