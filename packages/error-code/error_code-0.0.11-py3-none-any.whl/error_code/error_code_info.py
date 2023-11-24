from enum import Enum 

class StatusCodeEnum(Enum):
    """状态码枚举类型"""

    OK = (20000, '请求成功')
    Created = (20001, '创建成功')
    No_Content = (20004, '')
    Redirect = (30001, '重定向')
    Bad_Request = (40000, '请求失败')
    Unauthorized = (40001, '无权限')
    Forbidden = (40003, '请求被拒绝')
    Not_Found = (40004, '请求路径不存在')
    Method_Not_Allowed = (40005, '请求方法不正确')
    Unknow_Error = (40007, '未知错误')
    Request_Time_Out = (40008, '请求超时')
    SERVER_ERR = (50000, '服务器内部错误')
    Bad_Gateway = (50002, '从远端服务器获取请求')
    Service_Unavailable = (50003, '服务器暂时无法处理客户端的请求')
    Gateway_Time_Out = (50004, '代理网关未能从远端服务器获取请求')

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def errmsg(self):
        """获取状态信息"""
        return self.value[1]


if __name__ == "__main__":

    data = {"code":StatusCodeEnum.OK.code, "msg":StatusCodeEnum.OK.errmsg}