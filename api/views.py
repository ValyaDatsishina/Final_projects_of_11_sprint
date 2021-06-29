import uuid

from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitlesFilter
from api.models import User, Category, Genre, Titles, Review, Comments
from api.permissions import AdminOnly, AdminOnlyOrAuth, AdminUserOnly
from api.serializers import UserSerializer, EmailSerializer, ConfirmationSerializer, CategorySerializer, \
    GenreSerializer, TitleSerializer, TitleSlugSerializer, ReviewSerializer, CommentSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def send_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, email)
    send_mail(
        'Registration on YaMBL',
        f'Confirmation code to log in: {confirmation_code}',
        'admin@admin.ru',
        [email],
        fail_silently=False
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def take_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    confirmation_code = serializer.data['confirmation_code']
    code = str(uuid.uuid3(uuid.NAMESPACE_DNS, email))
    if code != confirmation_code:
        return Response({'confirmation_code': f'Confirmation code is incorrect'},
                        status=status.HTTP_400_BAD_REQUEST)
    username = email.rsplit('@')[0]
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, confirmation_code=confirmation_code)
        token = AccessToken.for_user(user)
        return Response({f'token: {token}'},
                        status=status.HTTP_200_OK)
    return Response({f'User exists'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly]
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']


class UserMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        user = get_object_or_404(self.queryset, email=request.user.email)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update_me(self, request):
        user = get_object_or_404(self.queryset, email=request.user.email)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(email=request.user.email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({f'Serializer is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def delete_me(self, request):
        user = get_object_or_404(self.queryset, email=request.user.email)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOnlyOrAuth]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOnlyOrAuth]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = [AdminOnlyOrAuth]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    # filter_backends = [SearchFilter]
    # search_fields = ['=category__slug', '=genre__slug', 'name', 'year', ]
    # filterset_fields = ['genre__slug', 'category__slug', 'name', 'year', ]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSlugSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AdminUserOnly, ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = Review.objects.filter(title_id=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        queryset = Review.objects.filter(title_id=title_id, author=self.request.user)
        if queryset.exists():
            raise ValidationError('You have already written review')
        serializer.save(author=self.request.user, title_id=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AdminUserOnly, ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter( review_id=review_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, id=title_id)
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review_id=review)


# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [AdminUserOnly]
#     pagination_class = PageNumberPagination
#
#     # def get_queryset(self):
#     def list(self, request, pk, review_id=None):
#         title = get_object_or_404(Titles, id=pk)
#         if review_id is None:
#             reviews = title.review
#             serializer = self.serializer_class(reviews, many=True)
#             return Response(serializer.data)
#         review = get_object_or_404(self.queryset, title_id=title, id=review_id)
#         serializer = self.serializer_class(review)
#         return Response(serializer.data)
#
#     def create(self, request, pk):
#         title = get_object_or_404(Titles, id=pk)
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(author=self.request.user, title_id=title)
#             return Response(serializer.data)
#         return Response(serializer.errors)
#
#     def update(self, request, pk, review_id):
#         title = get_object_or_404(Titles, id=pk)
#         review = get_object_or_404(self.queryset, title_id=title, id=review_id)
#         serializer = self.serializer_class(review, data=request.data)
#         if request.user == review.author or request.user.role in ['admin', 'moderator']:
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save(author=review.author, title_id=title)
#                 return Response(serializer.data)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     def delete(self, request, pk, review_id):
#         title = get_object_or_404(Titles, id=pk)
#         review = get_object_or_404(self.queryset, title_id=title, id=review_id)
#         if request.user == review.author or request.user.role in ['admin', 'moderator']:
#             review.delete()
#             return Response('Review removed', status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_403_FORBIDDEN)
