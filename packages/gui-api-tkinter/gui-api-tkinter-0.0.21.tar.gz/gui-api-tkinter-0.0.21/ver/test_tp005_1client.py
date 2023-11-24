import unittest

from pytest_ver import pth

from ver.helpers import services
from ver.helpers.helper import Helper


# -------------------
class TestTp005(unittest.TestCase):
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
        services.th.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp005(self):
        pth.proto.protocol('tp-005', 'check only 1 client can connect to the App server')
        pth.proto.add_objective('check that one and only one client can connect to the GUI API server')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{services.th.version}')

        pth.proto.step('start gui')
        services.helper.start_process()
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        ok = services.th.connect()
        pth.ver.verify_true(ok, reqids=['SRS-002'])
        pth.ver.verify_true(services.th.is_connected())

        pth.proto.step('attempt 2nd connection to GUI App server, should fail')
        ok = services.th.connect()
        pth.ver.verify_false(ok, reqids=['SRS-002'])
        pth.ver.verify_true(services.th.is_connected())

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
