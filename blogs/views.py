from rest_framework import generics, permissions, views, status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


# Vista para listar y crear posts con permisos
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Solo usuarios authenticates pueden crear posts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Vista para crear comentarios y respuesta
class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        parent_comment = None
        if 'parent_id' in self.kwargs:
            parent_comment = Comment.objects.get(id=self.kwargs['parent_id'])
        serializer.save(user=self.request.user, post=post, parent=parent_comment)


# vista para recuperar,actualizar y eliminar comentarios con restricciones de permisos
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo el autor puede modificar/eliminar su comentario

    def get_queryset(self):
        # Solo permitir que los usuarios vean/modifiquen sus propios comentarios
        return Comment.objects.filter(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Token deleted"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
