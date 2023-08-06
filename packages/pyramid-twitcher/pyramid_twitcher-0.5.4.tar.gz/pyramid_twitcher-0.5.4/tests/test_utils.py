import pytest
from lxml import etree
from twitcher import utils
from twitcher.exceptions import ServiceNotFound
from .common import WPS_CAPS_EMU_XML, WMS_CAPS_NCWMS2_111_XML, WMS_CAPS_NCWMS2_130_XML


def test_sanitize():
    assert utils.sanitize("Hummingbird") == "hummingbird"
    assert utils.sanitize("MapMint Demo Instance") == "mapmint_demo_instance"
    with pytest.raises(ValueError):
        assert utils.sanitize(None)
    with pytest.raises(ValueError):
        assert utils.sanitize("1", minlen=2)
    assert utils.sanitize(" ab c ") == "ab_c"
    assert utils.sanitize("a_much_to_long_name_for_this_test", maxlen=25) == "a_much_to_long_name_for_t"


def test_is_url_valid():
    assert utils.is_valid_url("http://somewhere.org") is True
    assert utils.is_valid_url("https://somewhere.org/my/path") is True
    assert utils.is_valid_url("file:///my/path") is True
    assert utils.is_valid_url("/my/path") is False
    assert utils.is_valid_url(None) is False


def test_parse_service_name():
    protected_path = '/ows/proxy'
    assert 'emu' == utils.parse_service_name("/ows/proxy/emu", protected_path)
    assert 'emu' == utils.parse_service_name("/ows/proxy/emu/foo/bar", protected_path)
    assert 'emu' == utils.parse_service_name("/ows/proxy/emu/", protected_path)
    with pytest.raises(ServiceNotFound):
        assert 'emu' == utils.parse_service_name("/ows/proxy/", protected_path)
    with pytest.raises(ServiceNotFound):
        assert 'emu' == utils.parse_service_name("/ows/nowhere/emu", protected_path)


def test_baseurl():
    assert utils.baseurl('http://localhost:8094/wps') == 'http://localhost:8094/wps'
    assert utils.baseurl('http://localhost:8094/wps?service=wps&request=getcapabilities') == 'http://localhost:8094/wps'
    assert utils.baseurl('https://localhost:8094/wps?service=wps&request=getcapabilities') ==\
        'https://localhost:8094/wps'
    with pytest.raises(ValueError):
        utils.baseurl('ftp://localhost:8094/wps')


def test_path_elements():
    assert utils.path_elements('/ows/proxy/lovely_bird') == ['ows', 'proxy', 'lovely_bird']
    assert utils.path_elements('/ows/proxy/lovely_bird/') == ['ows', 'proxy', 'lovely_bird']
    assert utils.path_elements('/ows/proxy/lovely_bird/ ') == ['ows', 'proxy', 'lovely_bird']


def test_lxml_strip_ns():
    import lxml.etree
    wpsxml = """
<wps100:Execute
xmlns:wps100="http://www.opengis.net/wps/1.0.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
service="WPS"
version="1.0.0"
xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsExecute_request.xsd"/>"""

    doc = lxml.etree.fromstring(wpsxml)
    assert doc.tag == '{http://www.opengis.net/wps/1.0.0}Execute'
    utils.lxml_strip_ns(doc)
    assert doc.tag == 'Execute'


def test_replace_caps_url_wps():
    doc = etree.parse(WPS_CAPS_EMU_XML)
    xml = etree.tostring(doc)
    assert b'http://localhost:8094/wps' in xml
    xml = utils.replace_caps_url(xml, "https://localhost/ows/proxy/emu")
    assert b'http://localhost:8094/wps' not in xml
    assert b'https://localhost/ows/proxy/emu' in xml


def test_replace_caps_url_wms_111():
    doc = etree.parse(WMS_CAPS_NCWMS2_111_XML)
    xml = etree.tostring(doc)
    assert b'http://localhost:8080/ncWMS2/wms' in xml
    xml = utils.replace_caps_url(xml, "https://localhost/ows/proxy/wms")
    # assert 'http://localhost:8080/ncWMS2/wms' not in xml
    assert b'https://localhost/ows/proxy/wms' in xml


def test_replace_caps_url_wms_130():
    doc = etree.parse(WMS_CAPS_NCWMS2_130_XML)
    xml = etree.tostring(doc)
    assert b'http://localhost:8080/ncWMS2/wms' in xml
    xml = utils.replace_caps_url(xml, "https://localhost/ows/proxy/wms")
    # assert 'http://localhost:8080/ncWMS2/wms' not in xml
    assert b'https://localhost/ows/proxy/wms' in xml
