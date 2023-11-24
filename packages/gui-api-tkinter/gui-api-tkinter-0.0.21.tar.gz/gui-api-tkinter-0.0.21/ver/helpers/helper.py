import sys
import time

from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from tools.debug_logger import DebugLogger as logger
from ver.helpers import services
from ver.helpers.cmd_runner import CmdRunner
from ver.helpers.logger_mock import Logger


# --------------------
class Helper:

    # --------------------
    def __init__(self):
        self.gui_process = None

        self.button1_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        self.label1_path = ['window1', 'page1_frame', 'button_frame', 'label1']
        self.menu_clear_path = [2]
        self.file_exit_path = [1, 2]

    # --------------------
    def init(self):
        services.logger = Logger()
        services.th = GuiApiHarness()
        services.th.init()

    # --------------------
    def term(self):
        services.th.term()

    # --------------------
    def init_each_test(self, ptobj):
        logger.line('')
        services.pytself = ptobj

    # --------------------
    def term_each_test(self):
        services.helper.kill_process()
        services.pytself.assertFalse(self.gui_process.is_alive())

        # uncomment for debugging
        # print(f'DBG {services.logger.lines}')

    # --------------------
    def start_process(self, args=''):
        services.logger.info(f'start_process: {args}')
        self.gui_process = CmdRunner()
        cmd = ''
        if sys.platform == 'win32':
            cmd = 'bash '
        cmd += f'ver/do_gui.sh {args}'
        self.gui_process.start_task_bg('gui', cmd, working_dir='.')
        # show it off for a bit
        time.sleep(1)

    # --------------------
    def kill_process(self):
        services.logger.info('kill_process')
        self.gui_process.finish()

    # --------------------
    def clean_shutdown(self):
        # do a clean exit of the GUI using File | Exit
        self.click_file_exit_menuitem()
        time.sleep(0.500)
        services.th.term()

    # --------------------
    @property
    def label1_text(self):
        item = services.th.search(self.label1_path)
        return item['value']

    # --------------------
    def click_button1(self):
        services.th.click_left(self.button1_path)

    # --------------------
    def click_clear_menuitem(self):
        services.th.menu_click(self.menu_clear_path)

    # --------------------
    def click_file_exit_menuitem(self):
        services.th.menu_click(self.file_exit_path)
