""" -- NETMANAGER -------
    Version: 1.0 14.02.21
    Author: Danila Kisluk
    [vk.com/danilakisluk]
    [dankis12a@gmail.com]
    ---------------------


    -- FUNCTIONAL -------
    netmanager.NetRequest
    ---------------------
"""


import ssl
ssl._create_default_https_context = ssl._create_unverified_context


from netmanager.netrequest import NetRequest
