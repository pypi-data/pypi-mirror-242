import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.constants import Constants
from ver.helpers import services
from ver.helpers.helper import Helper


# -------------------
class TestTp002(unittest.TestCase):
    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()
        services.helper = Helper()
        services.helper.init()

    # -------------------
    def setUp(self):
        services.helper.init_each_test(self)

    # -------------------
    def tearDown(self):
        services.helper.term_each_test()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        services.helper.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp002(self):
        pth.proto.protocol('tp-002', 'no callback defined, check for nak')
        pth.proto.add_objective('check that built-in functions work when callback funciton not defined')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        # use alternate access to version
        pth.proto.set_dut_version(f'v{Constants.version}')

        pth.proto.step('start gui')
        # don't define callback
        services.helper.start_process('--no-callback')
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected())

        pth.proto.step('send invalid "cmd02" command')
        cmd = {
            'cmd': 'cmd02',
            'param1': 'some parameter1',
            'param2': 'some parameter2',
        }
        rsp = services.th.send_recv(cmd)
        pth.ver.verify_equal(rsp['value'], 'nak', reqids='SRS-011')
        pth.ver.verify_equal(rsp['reason'], 'unknown command', reqids='SRS-011')

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
