from data_fetchers.mercury_mwb_210s import Mwb210S
from data_fetchers.page_aviability import PageAviabilityChecker
from data_fetchers.tplink_archer_c80 import TplinkArcherC80
from data_fetchers.zte_4g_router import ZteMF79U


DATA_FETCHERS = {
    "PageAviabilityChecker": PageAviabilityChecker,
    "TplinkArcherC80": TplinkArcherC80,
    "ZteMF79U": ZteMF79U,
    "Mwb210S": Mwb210S
}
