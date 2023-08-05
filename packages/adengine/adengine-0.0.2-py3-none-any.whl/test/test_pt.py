import pytest
import os
import unittest.mock as mock

from adengine.pt import *

from test import TEST_DATA, USE_VIRTUAL_DISPLAY


@pytest.fixture(scope='module')
def launch_packet_tracer_session():
    session = PacketTracerSession(use_virtual_display=USE_VIRTUAL_DISPLAY)
    session.start()
    yield session
    session.stop()


@pytest.mark.parametrize(
    ['filepath', 'password'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), '123', id='with_password'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'without_password.pka'), None, id='without_password'
        ),
    ]
)
def test_extract_data(filepath, password, launch_packet_tracer_session):
    extract_data(launch_packet_tracer_session, filepath, password)


@pytest.mark.parametrize(
    ['filepath', 'password', 'exception'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'no_such_file.pka'), None, ActivityFileReadingError, id='ActivityFileReadingError'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), 1234, WrongPassword, id='WrongPassword'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), None, ActivityNeedsPassword, id='ActivityNeedsPassword'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'topology.pkt'), None, TopologyFilesNotSupported, id='TopologyFilesNotSupported'
        ),
    ]
)
def test_extract_data_exceptions(filepath, password, exception, launch_packet_tracer_session):
    with pytest.raises(exception):
        extract_data(launch_packet_tracer_session, filepath, password)


def test_connection_failed(launch_packet_tracer_session):
    with mock.patch('adengine.pt.PacketTracerSession.port', new_callable=lambda: 80):
        with pytest.raises(ConnectionFailed):
            extract_data(launch_packet_tracer_session, os.path.join(TEST_DATA, 'without_password.pka'), None)
