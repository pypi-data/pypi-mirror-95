"""
ATTENTION:
These tests are not meant for the normal test case,
as this tries to test the integration to the Certbot by using
a subprocess call and installing this package globally.

You should not run this test unless you know exactly what you are doing.
"""
import os
import subprocess
import unittest

from certbot.errors import PluginError

from cert.client import Authenticator

DOMAIN = os.environ.get("TEST_DOMAIN")
DUCKDNS_TOKEN = os.environ.get("TEST_DUCKDNS_TOKEN")


class CertbotPluginTests(unittest.TestCase):

    def test_invalid_token(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        class TestConfig(object):
            test42_token = "securetoken42"

        auth = Authenticator(config=TestConfig(), name="test42")
        with self.assertRaises(PluginError):
            auth._perform(domain=DOMAIN, validation_name="test=42", validation="42")

    def test_empty_token(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        class TestConfig(object):
            test42_token = ""

        auth = Authenticator(config=TestConfig(), name="test42")
        with self.assertRaises(PluginError):
            auth._perform(domain=DOMAIN, validation_name="test=42", validation="42")

    def test_none_token(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        class TestConfig(object):
            test42_token = None

        auth = Authenticator(config=TestConfig(), name="test42")
        with self.assertRaises(PluginError):
            auth._perform(domain=DOMAIN, validation_name="test=42", validation="42")

    def test_invalid_domain(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        class TestConfig(object):
            test42_token = DUCKDNS_TOKEN

        auth = Authenticator(config=TestConfig(), name="test42")
        with self.assertRaises(PluginError):
            auth._perform(domain="thisdomainsisnotvalid", validation_name="test=42", validation="42")

    def test_certificate(self):
        assert DOMAIN is not None and len(DOMAIN) > 0
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        # check if certbot is installed
        subprocess.check_output(["certbot", "--version"])
        # install certbot_dns_duckdns plugin
        subprocess.check_output(["pip", "install", ".."])
        # check if certbot works properly with the dns plugin
        subprocess.check_output(["certbot",
                                 "certonly",
                                 "--non-interactive",
                                 "--agree-tos",
                                 "--register-unsafely-without-email",
                                 "--authenticator",
                                 "dns-duckdns",
                                 "--dns-duckdns-token",
                                 DUCKDNS_TOKEN,
                                 "--dns-duckdns-propagation-seconds",
                                 "60",
                                 "--dry-run",
                                 "-d",
                                 DOMAIN,
                                 # change the output dirs to allow running test without root permission
                                 "--work-dir",
                                 "test_certbot/config",
                                 "--config-dir",
                                 "test_certbot/config",
                                 "--logs-dir",
                                 "test_certbot/logs"])

    def test_wildcard_certificate(self):
        assert DOMAIN is not None and len(DOMAIN) > 0 and DOMAIN[0] not in [".", "*"]
        assert DUCKDNS_TOKEN is not None and len(DUCKDNS_TOKEN) > 0

        wildcard_domain = "*.{}".format(DOMAIN)

        # check if certbot is installed
        subprocess.check_output(["certbot", "--version"])
        # install certbot_dns_duckdns plugin
        subprocess.check_output(["pip", "install", ".."])
        # check if certbot works properly with the dns plugin
        subprocess.check_output(["certbot",
                                 "certonly",
                                 "--non-interactive",
                                 "--agree-tos",
                                 "--register-unsafely-without-email",
                                 "--authenticator",
                                 "dns-duckdns",
                                 "--dns-duckdns-token",
                                 DUCKDNS_TOKEN,
                                 "--dns-duckdns-propagation-seconds",
                                 "60",
                                 "--dry-run",
                                 "-d",
                                 wildcard_domain,
                                 # change the output dirs to allow running test without root permission
                                 "--work-dir",
                                 "test_certbot/config",
                                 "--config-dir",
                                 "test_certbot/config",
                                 "--logs-dir",
                                 "test_certbot/logs"])


if __name__ == "__main__":
    unittest.main()
