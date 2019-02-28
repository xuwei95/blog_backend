def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""

    return {
        'code': 20000,
        'data': {'token': token}
    }
