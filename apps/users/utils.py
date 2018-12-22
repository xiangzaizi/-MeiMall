
def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token: 生成token令牌
    :param user: 前面验证通过以后得到的用户模型对象
    :param request: 本次用户提交请求信息
    :return: 前段希望提供的数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }
