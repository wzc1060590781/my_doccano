from rest_framework.permissions import BasePermission


class RegisterPermission(BasePermission):
    # 无权限的显示信息
    message = '您没有权限查看'

    # 必须重写 has_permission
    def has_permission(self, request, view):
        user_type = request.user.role_id
        # user_type_name = request.user.get_user_type_display()
        # print(request.user.name)
        # print(user_type_name)
        print("has_permission")
        if user_type == 2:
            return True
        else:
            return False
