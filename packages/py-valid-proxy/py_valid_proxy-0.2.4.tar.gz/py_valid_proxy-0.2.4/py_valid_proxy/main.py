# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg
# @Date:   2023-11-13 11:20:47
# @Last Modified by:   Suvorinov Oleg
# @Last Modified time: 2023-11-19 20:14:49

import argparse
import logging
from urllib.parse import urlparse
import pkg_resources

from py_valid_proxy import valid_proxy

logger = logging.getLogger(__name__)


def main(args=None):

    _prog = "%(prog)s"
    _version = pkg_resources.get_distribution('py_valid_proxy').version
    _prog_version = f"{_prog} {_version}"

    parser = argparse.ArgumentParser(
        prog='valid_proxy',
        description="Valid the functionality of the proxy server"
    )

    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=5,
        help='The connect timeout is the number of seconds')

    parser.add_argument(
        "-l", "--log",
        help="Console logs",
        action="store_false"
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=_prog_version
    )

    parser.add_argument(
        'proxy',
        help='URL of proxy server'
    )

    args = parser.parse_args()

    timeout = 5
    if args.timeout:
        timeout = args.timeout

    if not args.log:
        logging.basicConfig(level=logging.INFO)

    if args.proxy:
        result = urlparse(args.proxy.lower())
        if not result.scheme or \
                not result.netloc or \
                not result.hostname or \
                not result.port:
            raise ValueError(
                str(args.proxy) + " is not in http(s)://hostname:port format")

        valid = " ... is dead"
        try:
            proxy_info = valid_proxy(
                result.hostname,
                result.port,
                result.scheme,
                timeout)
        except Exception as e:
            logger.info(" {error}".format(error=str(e)))
        else:
            if not args.log:
                print('Host: {}'.format(proxy_info['host']))
                print('Port: {}'.format(proxy_info['port']))
                print('Scheme: {}'.format(proxy_info['scheme']))
                print('Response time: {}'.format(proxy_info['response_time']))
                print('Export address: {}'.format(proxy_info['export_address'])) # noqa
                print('Anonymity: {}'.format(proxy_info['anonymity']))
                print('Country : {}'.format(proxy_info['country']))
            valid = " ... alive"
        finally:
            print(f"{args.proxy}{valid}")


if __name__ == '__main__':
    main()
