import unittest

from pytest_ver import pth

from ver.helpers import services
from ver.helpers.helper import Helper


# -------------------
class TestTp004(unittest.TestCase):
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
    def test_tp004(self):
        pth.proto.protocol('tp-004', 'check "search" with various invalid paths')
        pth.proto.add_objective('check that search respond with accurate nak JSON objects')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{services.th.version}')

        pth.proto.step('start gui')
        # don't call callback
        services.helper.start_process()
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected())

        # no get_screen at this point

        pth.proto.step('with no get_screen, search using a valid path')
        button_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        item = services.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-024'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-024'])
        pth.ver.verify_equal('content is None', item['reason'], reqids=['SRS-024'])

        pth.proto.step('get page content')
        services.th.get_screen()
        pth.ver.verify_gt(len(services.th.content), 0)

        pth.proto.step('search using a valid path to button1')
        button_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        item = services.th.search(button_path)
        self.assertEqual(item['value'], 'press me!')

        pth.proto.step('check if 1st item in path is not found')
        button_path = ['windowx', 'page1_frame', 'button_frame', 'button1']
        item = services.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is not found', item['reason'], reqids=['SRS-025'])

        pth.proto.step('check if middle item in path is not found')
        button_path = ['window1', 'pagex_frame', 'page']
        item = services.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is not found', item['reason'], reqids=['SRS-025'])

        pth.proto.step('check if last item in path is not found')
        button_path = ['window1', 'page_frame', 'pagex']
        item = services.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is not found', item['reason'], reqids=['SRS-025'])

        pth.proto.step('check if path is an empty list')
        button_path = []
        item = services.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is empty', item['reason'], reqids=['SRS-025'])

        pth.proto.step('check if search path list is None')
        button_path = None
        item = services.th.search(button_path)
        pth.ver.verify_equal('search', item['rsp'], reqids=['SRS-025'])
        pth.ver.verify_equal('nak', item['value'], reqids=['SRS-025'])
        pth.ver.verify_equal('search path is None', item['reason'], reqids=['SRS-025'])

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
