# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg
# @Date:   2023-11-13 10:16:09
# @Last Modified by:   Suvorinov Oleg
# @Last Modified time: 2023-11-19 14:03:49

__author__ = 'Oleg Suvorinov'
__email__ = 'suvorinovoleg@yandex.ru'
__version__ = '0.1.0'


from .valid_proxy import valid_proxy, ValidProxyException

__all__ = (
    'valid_proxy',
    'ValidProxyException'
)
