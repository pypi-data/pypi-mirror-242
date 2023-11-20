import unittest
from unittest.mock import patch, MagicMock
from opsys_ps_controller.ps_controller import PsController


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(PsController, 'init_connection')
    def test_init_connection(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.init_connection()
        ps_mock.assert_called_once_with()

    @ patch.object(PsController, 'is_connected')
    def test_is_connected(self, ps_mock: MagicMock):
        ps_conn = PsController()
        port = 'COM3'
        ps_conn.is_connected(port=port)
        ps_mock.assert_called_once_with(port='COM3')
        
    @ patch.object(PsController, 'disconnect')
    def test_disconnect(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.disconnect()
        ps_mock.assert_called_once_with()

    @ patch.object(PsController, 'ps_on')
    def test_ps_on(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.ps_on()
        ps_mock.assert_called_once_with()

    @ patch.object(PsController, 'ps_off')
    def test_ps_off(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.ps_off()
        ps_mock.assert_called_once_with()

    @ patch.object(PsController, 'ps_reset')
    def test_ps_reset(self, ps_mock: MagicMock):
        ps_conn = PsController()
        delay = 20
        ps_conn.ps_reset(reset_delay=delay)
        ps_mock.assert_called_once_with(reset_delay=20)

    @ patch.object(PsController, 'get_current')
    def test_get_current(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.get_current()
        ps_mock.assert_called_once_with()

    @ patch.object(PsController, 'set_current')
    def test_set_current(self, ps_mock: MagicMock):
        ps_conn = PsController()
        current = 2
        ps_conn.set_current(current=current)
        ps_mock.assert_called_once_with(current=2)

    @ patch.object(PsController, 'get_voltage')
    def test_get_voltage(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.get_voltage()
        ps_mock.assert_called_once_with()

    @ patch.object(PsController, 'set_voltage')
    def test_set_voltage(self, ps_mock: MagicMock):
        ps_conn = PsController()
        voltage = 12
        ps_conn.set_voltage(voltage=voltage)
        ps_mock.assert_called_once_with(voltage=12)

    @ patch.object(PsController, 'is_remote')
    def test_is_remote(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.is_remote()
        ps_mock.assert_called_once_with()

    @ patch.object(PsController, 'set_mode')
    def test_set_mode(self, ps_mock: MagicMock):
        ps_conn = PsController()
        remote_enable = True
        ps_conn.set_mode(is_remote=remote_enable)
        ps_mock.assert_called_once_with(is_remote=True)

    @ patch.object(PsController, 'set_ps_address')
    def test_set_ps_address(self, ps_mock: MagicMock):
        ps_conn = PsController()
        address = 1
        ps_conn.set_ps_address(address=address)
        ps_mock.assert_called_once_with(address=1)

    @ patch.object(PsController, 'read_buffer')
    def test_read_buffer(self, ps_mock: MagicMock):
        ps_conn = PsController()
        header = b"AA"
        ps_conn.read_buffer(remove_header=header)
        ps_mock.assert_called_once_with(remove_header=b"AA")

    @ patch.object(PsController, 'init_buffer')
    def test_init_buffer(self, ps_mock: MagicMock):
        ps_conn = PsController()
        ps_conn.init_buffer()
        ps_mock.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
