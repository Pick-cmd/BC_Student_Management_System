# GPacket模块，用在客户端和服务器之间进行通讯交互
# 包括Packet_operate和Packet_result，
# 操作信号有以下几种
# l: 登录
# d: 删除某个用户的信息，需要使用setter设置被删除的用户
# a: 增加一条用户信息，需要使用setter设置新添的用户
# s: 请求获取相应用户权限的信息
# u：更新一条信息，，需要使用setter设置被更新的用户

import GUser


class Packet_operate:
    def __init__(self):
        self.__operate_type = None
        self.__operator = GUser.GroupMember()

    def setOperator(self, operator: GUser.GroupMember):
        self.__operator = operator

    def setOperate_type(self, operate_type: str):
        self.__operate_type = operate_type

    def getOperate_type(self):
        return self.__operate_type

    def getOperator(self) -> GUser.GroupMember:
        return self.__operator


class Packet_login(Packet_operate):
    def __init__(self):
        super(Packet_login, self).__init__()
        self.setOperate_type('l')


# problem : 泛化问题
class Packet_add_info(Packet_operate):
    def __init__(self):
        super(Packet_add_info, self).__init__()
        self.setOperate_type('a')
        self.__add_info = None

    def setAdd_information(self, add_info: GUser.GroupMember):
        self.__add_info = add_info

    def getAdd_info(self) -> GUser.GroupMember:
        return self.__add_info


class Packet_update_info(Packet_operate):
    def __init__(self):
        super(Packet_update_info, self).__init__()
        self.setOperate_type('u')
        self.__update_info = None

    def setUpdate_info(self, update_info: GUser.GroupMember):
        self.__update_info = update_info

    def getUpdate_info(self) -> GUser.GroupMember:
        return self.__update_info


class Packet_delete_info(Packet_operate):
    def __init__(self):
        super(Packet_delete_info, self).__init__()
        self.setOperate_type('d')
        self.__delete_info = None

    def setUpdate_info(self, delete_info: GUser.GroupMember):
        self.__delete_info = delete_info

    def getUpdate_info(self) -> GUser.GroupMember:
        return self.__delete_info


class Packet_search_info(Packet_operate):
    def __init__(self):
        super(Packet_search_info, self).__init__()
        self.setOperate_type('s')
