import pytest
import unittest
from tempfile import mkdtemp

from twitcher.esgf import ESGFAccessManager


@pytest.mark.skip(reason="fix test")
class ESGFTestCase(unittest.TestCase):
    def setUp(self):
        import mock
        self.mgr = ESGFAccessManager(
            slcs_service_url="https://localhost:5000",
            base_dir=mkdtemp())
        self.mgr._retrieve_certificate = mock.MagicMock(return_value=True)

    def test_logon_with_token(self):
        assert self.mgr.logon(access_token="abcdef") is True
