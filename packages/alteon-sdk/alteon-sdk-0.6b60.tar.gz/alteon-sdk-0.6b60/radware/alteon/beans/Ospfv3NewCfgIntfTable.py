
from radware.sdk.beans_common import *


class EnumOspfv3IntfState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfv3IntfDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Ospfv3NewCfgIntfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Id = kwargs.get('Id', None)
        self.AreaId = kwargs.get('AreaId', None)
        self.Priority = kwargs.get('Priority', None)
        self.Cost = kwargs.get('Cost', None)
        self.Hello = kwargs.get('Hello', None)
        self.Dead = kwargs.get('Dead', None)
        self.Transit = kwargs.get('Transit', None)
        self.Retrans = kwargs.get('Retrans', None)
        self.State = EnumOspfv3IntfState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfv3IntfDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

