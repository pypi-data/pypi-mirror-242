import pandas as pd
from typing import List, Union
from functools import lru_cache
from .constants import NetValueData
from gytoolkit import ppwdbapi
from gytoolkit.mailparser import MailClient
from gytoolkit.utils import load_netvalue,save_netvalue
from .utils import get_otc_nv, ppwnvformatter


class NetValueManager:
    def __init__(self) -> None:
        self.api = {}
        self.api["mail"] = {}

    def set_ppwdbapi(self, username, password, addr):
        ppwdbapi.login(username=username, password=password, addr=addr)
        self.api["ppwdbapi"] = ppwdbapi

    def set_mailapi(self, username, password):
        mailclient = MailClient(username=username, password=password)
        self.api["mail"][username] = mailclient

    def update_local_mail(self, depth=50):
        if not hasattr(self, "local_mail_file"):
            raise ValueError("Please set local mail file first.")
        
        local_mail_file = self.local_mail_file
        mail_api = self.api.get("mail")
        if len(mail_api) > 0:
            for mailaccount, api in mail_api.items():
                headers = api.get_mail_header(lookin_depth=depth)
                nv_list = api.parse_mails(headers)
                save_netvalue(nv_list, local_mail_file)
        self.set_local_mail(local_mail_file)

    def set_local_mail(self, local_mail_file):
        self.local_mail_file = local_mail_file
        self.get_local.cache_clear()
    
    def set_local_otc(self, otc_folder_path):
        self.otc_folder_path = otc_folder_path
        self.get_local.cache_clear()
    
    def set_addtional_file(self, additional_file):
        self.additional_file = additional_file
        self.get_local.cache_clear()

    @lru_cache
    def get_local(
        self, df=True
    ) -> List[NetValueData]:
        # 按优先级顺序读取数据
        # 1、OTC数据
        if hasattr(self, "otc_folder_path"):
            otc_netvalues = get_otc_nv(self.otc_folder_path, df=True)
        else:
            otc_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])
        # 2、手工净值
        if hasattr(self, "additional_file"):
            addtional_netvalues = load_netvalue(self.additional_file, df=True)
        else:
            addtional_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])
        # 3、邮箱数据
        if hasattr(self, "local_mail_file"):
            mail_netvalues = load_netvalue(self.local_mail_file, df=True)
        else:
            mail_netvalues = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

        local_netvalues = otc_netvalues.combine_first(addtional_netvalues)
        local_netvalues = local_netvalues.combine_first(mail_netvalues)

        if df:
            return local_netvalues
        else:
            return [NetValueData(**row) for index, row in local_netvalues.reset_index().iterrows()]

    def get_netvalue(
        self,
        prodcode,
        df=True,
    ) -> Union[List[NetValueData], pd.DataFrame]:
        local_netvalues = self.get_local()
        idx = pd.IndexSlice
        try:
            local_netvalue = local_netvalues.loc[idx[:, prodcode],]
        except:
            local_netvalue = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

        ppwdbapi = self.api.get("ppwdbapi")
        if ppwdbapi:
            fund_info = ppwdbapi.get_fund(reg_ids=prodcode)
            ppwnv = ppwnvformatter(ppwdbapi.get_netvalue(fund_info.index))
        else:
            ppwnv = pd.DataFrame(columns=NetValueData.__dataclass_fields__.keys()).set_index(keys=['date', 'prodcode'])

        net_value = ppwnv.combine_first(local_netvalue)
        if df:
            return net_value
        else:
            return [NetValueData(**row) for index, row in net_value.reset_index().iterrows()]
