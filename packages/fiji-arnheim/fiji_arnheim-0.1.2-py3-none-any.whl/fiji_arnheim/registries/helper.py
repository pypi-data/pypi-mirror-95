import imagej

class BaseImageJHelper:

    def __init__(self, headless=False, version="2.1.0", plugins= []) -> None:
        # concatenade version plus plugins
        build = [version] + plugins if len(plugins) > 0 else version

        self._ij = imagej.init(build, headless=headless)
        if not headless: self._ij.ui().showUI()
        super().__init__()
    
    @property
    def py(self):
        return self._ij.py

    @property
    def ui(self):
        return self._ij.ui()

    @property
    def ij(self):
        return self._ij

RUNNING_HELPER = None

def get_running_helper() -> BaseImageJHelper:
    global RUNNING_HELPER
    if RUNNING_HELPER is None:
        RUNNING_HELPER = BaseImageJHelper()
    return RUNNING_HELPER

def set_running_helper(instance: BaseImageJHelper):
    global RUNNING_HELPER
    RUNNING_HELPER = instance