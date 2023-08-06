# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 20:52:33 2015

@author: SW274998
"""
from nseta.common.commons import *
import datetime
import unittest
import time

from bs4 import BeautifulSoup
from tests import htmls
import json
import requests
import six
from nseta.common.urls import *
import nseta.common.urls as urls
from six.moves.urllib.parse import urlparse
from baseUnitTest import baseUnitTest

class TestUrls(baseUnitTest):
    def setUp(self, redirect_logs=True):
        super().setUp()
        proxy_on = False
        if proxy_on:
            urls.session.proxies.update({'http': 'proxy1.wipro.com:8080'})

    def runTest(self):
        for key in TestUrls.__dict__.keys():
            if key.find('test') == 0:
                TestUrls.__dict__[key](self)

    def test_get_symbol_count(self):
        count = get_symbol_count(symbol='SBIN')
        self.assertEqual(count, '1')
        force_count = get_symbol_count(symbol='SBIN', force_refresh=True)
        self.assertEqual(force_count, '1')

    def test_equity_history_url(self):
        sym_count = get_symbol_count(symbol='SBIN')
        txt = 'Data for SBIN - EQ'
        resp = equity_history_url(symbol='SBIN',
                                  symbolCount=sym_count,
                                  series='EQ',
                                  fromDate='01-01-2000',
                                  toDate='10-01-2000',
                                  dateRange='')
        self.assertGreaterEqual(resp.text.find(txt), 0, resp.text)

    def test_nse_intraday_url(self):
        txt = 'date|g1_o|g1_h|g1_l|g1_c|g2|g2_CUMVOL' #'<columns><column>date</column><column>pltp</column><column>nltp</column><column>previousclose</column><column>allltp</column>'
        resp = nse_intraday_url(CDSymbol='SBIN', Periodicity="1")
        self.assertIn(txt, resp.text)

    def test_price_list_url(self):
        resp = price_list_url('2019', 'DEC', '31DEC2019')
        csv = unzip_str(resp.content)
        self.assertGreaterEqual(csv.find('SBIN'), 0)

    def tests_daily_volatility_url(self):
        resp = daily_volatility_url("19112015")
        self.assertGreaterEqual(resp.text.find('SBIN'), 0)

    def test_pr_price_list_zipped_url(self):
        resp = pr_price_list_zipped_url('191115')
        csv = unzip_str(resp.content)

    def test_index_history_url(self):
        resp = index_history_url(indexType="NIFTY 50",
                                 fromDate="01-01-2015",
                                 toDate="10-01-2015")
        self.assertGreaterEqual(resp.text.find('High'), 0)
        self.assertGreaterEqual(resp.text.find('Low'), 0)

    def test_index_daily_snapshot_url(self):
        resp = index_daily_snapshot_url("06012020")
        csv = str(resp.content)
        self.assertGreaterEqual(csv.find('Nifty 50'), 0)
        self.assertGreaterEqual(csv.find('Nifty IT'), 0)
        self.assertGreaterEqual(csv.find('Nifty Bank'), 0)
        self.assertGreaterEqual(csv.find('Nifty Next 50'), 0)

    def test_index_pe_history_url(self):
        resp = index_pe_history_url(fromDate="01-01-2015",
                                    toDate="10-01-2015",
                                    indexName="NIFTY 50")
        self.assertGreaterEqual(resp.text.find('<th>P/E'), 0)
        self.assertGreaterEqual(resp.text.find('<th>P/B'), 0)

    def test_index_vix_history_url(self):
        resp = index_vix_history_url(fromDate="01-Jan-2015",
                                     toDate="10-Jan-2015",
                                     )
        self.assertGreaterEqual(resp.text.find('VIX'), 0)
        self.assertGreaterEqual(resp.text.find('Change'), 0)

    def test_derivative_derivative_expiry_dates_url(self):
        resp = derivative_expiry_dates_url()
        self.assertGreaterEqual(resp.text.find('vixExpryDt'), 0)

    def test_derivative_history_url(self):
        resp = derivative_history_url(instrumentType="FUTIDX",
                                      symbol="NIFTY",
                                      expiryDate="26-12-2019",
                                      optionType="select",
                                      strikePrice='',
                                      dateRange='',
                                      fromDate='25-Dec-2019',
                                      toDate="26-Dec-2019")
        self.assertGreaterEqual(resp.text.find('NIFTY'), 0)
        self.assertGreaterEqual(resp.text.find('Expiry'), 0)

    def test_derivative_price_list_url(self):
        resp = derivative_price_list_url('2019', 'JUL', '19JUL2019')
        csv = unzip_str(resp.content)

    def tearDown(self):
        super().tearDown()

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestUrls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if six.PY2:
        if result.wasSuccessful():
            print("tests OK")
        for (test, error) in result.errors:
            print("=========Error in: %s===========" % test)
            print(error)
            print("======================================")

        for (test, failures) in result.failures:
            print("=========Error in: %s===========" % test)
            print(failures)
            print("======================================")
