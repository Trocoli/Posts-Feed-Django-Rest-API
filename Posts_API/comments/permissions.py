from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
     permissão customizada para checar se usuário é o dono do post, só este ou um admin pode editar ou deletar um post 
    """
    message = "Você precisa ser o autor da postagem para fazer alterações nela."
    my_safe_method = ['GET','PUT', 'DELETE']

    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False 


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user