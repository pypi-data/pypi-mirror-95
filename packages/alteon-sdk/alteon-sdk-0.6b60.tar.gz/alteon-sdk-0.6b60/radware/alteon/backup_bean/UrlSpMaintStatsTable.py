
from radware.sdk.beans_common import *


class UrlSpMaintStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.CurMemUnits = kwargs.get('CurMemUnits', None)
        self.LowestMemUnits = kwargs.get('LowestMemUnits', None)

    def get_indexes(self):
        return self.SpIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex',

