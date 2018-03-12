#!/usr/bin/env python
import logging
from urlparse import urljoin

import simplejson as json
from requests import Session


class API(object):
    ''' Manages the connection to CryptoKred 3Scale API.'''

    def __init__(self, dev_key=None):
        self._request = Session().request
        self.base = 'https://cryptokred-2445581407604.apicast.io:443'

        self.dev_key = dev_key

        self.request = self.Caller(self.cryptokred_request)


    def cryptokred_request(self,
                url,
                method='GET',
                token=None,
                data=None,
                headers=None,
                return_status=False,
                **keywords):

        if data is None:
            data = {}

        if not 'dev_key' in data:
            data['dev_key'] = self.dev_key

        if not token is None:
            data['token'] = token

        if headers is None:
            headers = {}

        # Data
        if keywords:
            data.update(keywords)

        if method == 'GET':
            params = data
        else:
            params = None

        # if data is not None:
        #     data = json.dumps(data)

        if headers is not None:
            for k in headers:
                if not isinstance(headers[k]) == str:
                    headers[k] = str(headers[k])

        logging.debug('url %s' % url)

        url = urljoin(self.base, 'coin/%s' % url)

        logging.debug('url %s' % url)

        # Make the request
        logging.debug('CryptoKred request: method:%s url:%s headers:%s data:%s',
                      method, url, headers, data)


        response = self._request(method=method, url=url, data=data, params=params, headers=headers)
        text = response.text
        status = response.status_code

        try:
            data = json.loads(text)
            if status >= 400:
                try:
                    message = data['message'] if 'message' in data else data['error']
                    logging.error('SocialOS error: %s: %s', message, data['request'])
                    if 'traceback' in data:
                        logging.error('Server traceback:\n%s', data['traceback'].strip())
                except KeyError:
                    logging.error('SocialOS error:\n%s', json.dumps(data, indent=2))

        except json.JSONDecodeError as exception:
            logging.error('json error:%s\nbad json:"%s"', exception, text)
            raise

        if return_status:
            data = data, status

        return data


    class Caller(object):
        ''' This class wraps access to the request function and provides a
            slightly more natural interface allowing the user to specify the method/verb as callable attribute.
            Examples:

            self.request('coins') # does method=GET
            self.request.get('coins') # does method=GET too
            self.request.post('register', data=data) # does method=POST using admin_request
        '''
        def __init__(self, request):
            self.request = request

        def __getattr__(self, key):
            method = key.upper()
            def function(*arguments, **keywords):
                return self.request(*arguments, method=method, **keywords)
            setattr(self, key, function)
            return function

        def __call__(self, *arguments, **keywords):
            if len(arguments) > 1:
                keywords['method'] = arguments[0]
                arguments = arguments[1:]
            return self.request(*arguments, **keywords)


