# -*- coding: utf-8 -*-
import inspect
from functools import wraps
from string import Formatter

from easi_py_common.client.rest_client import RestClient, DST_MODE_SERVICE

service_endpoint = {}

HTTP_METHOD_GET = 'GET'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_DELETE = 'DELETE'


def service_client(url, timeout=(5, 5), http_adapter=None, before_request=None,
                   dst_mode=DST_MODE_SERVICE):
    def wrapper(f):
        key = '{}.{}'.format(f.__module__, f.__name__)

        service_endpoint[key] = RestClient(
            url, timeout=timeout, http_adapter=http_adapter, before_request=before_request,
            dst_mode=dst_mode)

        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def service_mapping(uri, method, timeout=None, request_by_alias: bool = True, body_key='data'):
    def wrapper(f):
        full_arg_spec = inspect.getfullargspec(f)
        is_method = full_arg_spec.args and full_arg_spec.args[0] == 'self'
        if not is_method:
            raise Exception('{} is invalid service_mapping', f.__name__)

        dst = full_arg_spec.annotations.get('return')
        has_format_names = [fn for _, fn, _, _ in Formatter().parse(uri) if fn is not None]

        def __get_request_params(named_args):
            request_named_args = {k: v for k, v in named_args.items() if k not in has_format_names}
            data = {}
            if method == HTTP_METHOD_POST or method == HTTP_METHOD_PUT:
                if body_key in request_named_args:
                    data = request_named_args.get(body_key)
                    request_named_args.pop(body_key)
            return request_named_args, data

        @wraps(f)
        def wrapped(*args, **kwargs):
            name = '{}.{}'.format(args[0].__class__.__module__, args[0].__class__.__name__)
            if name not in service_endpoint:
                raise Exception('{}.{} is not have config endpoint', f.__module__, f.__name__)

            named_args = inspect.getcallargs(f, *args, **kwargs)
            named_args.update(named_args.pop(full_arg_spec.varkw, {}))

            _uri = uri.format(**named_args)
            params, data = __get_request_params(named_args)

            client = service_endpoint[name]
            if method == HTTP_METHOD_GET:
                return client.get(_uri, params=params, timeout=timeout, dst=dst)
            elif method == HTTP_METHOD_POST:
                return client.post(_uri, json_data=data, params=params, timeout=timeout, dst=dst,
                                   request_by_alias=request_by_alias)
            elif method == HTTP_METHOD_PUT:
                return client.put(_uri, json_data=data, params=params, timeout=timeout, dst=dst,
                                  request_by_alias=request_by_alias)
            elif method == HTTP_METHOD_DELETE:
                return client.delete(_uri, params=params, timeout=timeout, dst=dst)
            else:
                raise Exception('{}.{} is invalid method', f.__module__, f.__name__)

        return wrapped

    return wrapper
