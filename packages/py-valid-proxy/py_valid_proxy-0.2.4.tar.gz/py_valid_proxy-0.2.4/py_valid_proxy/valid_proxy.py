# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg
# @Date:   2023-11-19 13:52:25
# @Last Modified by:   Suvorinov Oleg
# @Last Modified time: 2023-11-20 18:04:17

import os
import time
from typing import Dict
import json

import geoip2.database
import requests

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"  # noqa


class ValidProxyException(
        requests.exceptions.MissingSchema,
        requests.exceptions.InvalidSchema,
        requests.exceptions.ReadTimeout,
        requests.exceptions.InvalidProxyURL,
        requests.exceptions.ProxyError,
        requests.exceptions.JSONDecodeError):
    pass


def get_origin_ip(timeout: int = 5) -> str:
    try:
        resp = requests.get(
            'http://httpbin.org/get',
            headers={"User-Agent": USER_AGENT},
            timeout=timeout
        ).json()
    except ValidProxyException:
        return ''
    return resp.get('origin', '')


def valid_proxy(
        host: str,
        port: int,
        scheme: str = 'http',
        timeout: int = 5) -> Dict:
    """Valid proxy server ('alive' or 'dead')

    Parameters
    ----------
    host : str
        IP Address
    port : int
        Port
    scheme: str, optional
        Scheme (default is 'http')
    timeout: int, optional
        Connect timeout is number of seconds (default is 5 sec.)
    Returns
    -------
        None if proxy is 'dead'
        dict if proxy is 'alive'
        {
            "scheme": str, # http, https
            "host": str,
            "port": int,
            "export_address": list[str],
            "anonymity": str, # transparent, anonymous, high_anonymous # noqa
            "country": str # ISO Code 
            "response_time": float
        }
    """
    _proxy = dict()
    origin_ip = get_origin_ip()

    def _anonymity(origin_ip, response):
        via = response.get('headers', {}).get('Via', '')

        if origin_ip in json.dumps(response):
            return 'transparent'
        elif via and via != "1.1 vegur":
            return 'anonymous'
        else:
            return 'high_anonymous'

    def _export_address(origin_ip, response):
        origin = response.get('origin', '').split(', ')
        if origin_ip in origin:
            origin.remove(origin_ip)
        return origin

    def _country(host):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        try:
            geoip_reader = geoip2.database.Reader(
                os.path.join(base_dir, 'data/GeoLite2-Country.mmdb')
            )
            country = geoip_reader.country(host).country.iso_code
        except Exception:
            country = "unknown"
        return country

    request_begin = time.time()

    request_proxies = {
        scheme: "%s:%s" % (host, port)
    }
    url = "%s://httpbin.org/get?show_env=1&cur=%s" % ('http', request_begin)
    try:
        _r = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            proxies=request_proxies,
            timeout=timeout
        ).json()
    except ValidProxyException:
        return None

    request_end = time.time()

    _proxy["scheme"] = scheme
    _proxy["host"] = host
    _proxy["port"] = port
    _proxy["export_address"] = _export_address(origin_ip, _r)
    _proxy["anonymity"] = _anonymity(origin_ip, _r)
    _proxy["country"] = _country(host)
    _proxy["response_time"] = round(request_end - request_begin, 2)

    return _proxy
