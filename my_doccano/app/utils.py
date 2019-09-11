def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    # print("jwt_response_payload_handler")
    print("user.role_id",user.role_id)
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        "role_id" : user.role_id
    }