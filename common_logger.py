'''
*************************************************************************************
* @developer        :   Nihal Chandrasiri
* @developer email  :   ncr5630@gmail.com
* @licence          :   GNU/GPL
* @product          :   1billion Technology Test
* @date             :   Feb 2023
* ************************************************************************************ *
'''

# -*- coding: utf-8 -*-
# !/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals
import logging
import logging.handlers
import datetime
from datetime import datetime
from xmlrpc.client import boolean


class CommonLogger:
    def __init__(self) -> str:
        self.loginfo = True
        self.com_logger = None
        self.log_filename = None
        dateTimeObj = datetime.now()
        self.log_datetime = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")

    def manage_logger(self, level, cus_message=None, sys_message=None, class_name=None) -> boolean:

        return_val = False
        loginfo = self.loginfo
        if cus_message or sys_message:
            logging_message = "Custom_message : %s, System_message:%s, Class_name:%s" % ( \
                cus_message, sys_message, class_name)
            com_logger = logging.getLogger('1bT_logger')
            if level == "info" and loginfo:
                com_logger.setLevel(logging.INFO)
                com_logger.info(logging_message)
                return_val = True

            elif level == "warning":
                com_logger.setLevel(logging.WARNING)
                com_logger.warning(logging_message)
                return_val = True

            elif level == "error":
                com_logger.setLevel(logging.ERROR)
                com_logger.error(logging_message)
                return_val = True

            elif level == "critical":
                com_logger.setLevel(logging.CRITICAL)
                com_logger.critical(logging_message)
                return_val = True

        return return_val
