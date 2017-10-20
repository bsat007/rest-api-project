# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions
# Create your views here.


class HelloApiView(APIView):
    """Test API View."""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""


        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional Django View',
             'Gives you the most control over your logic',
             'Is mapped manually to URLs'
        ]


        return Response({'message': 'Hello!', 'an_apiview': an_apiview})


    def post(self, request):
        """
        Create a Hello message with our name.
        """

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
    else:
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Handles updating an object.
        """

        return Response({'method':"put"})

    def patch(self, request, pk=None):
        """
        Patch request, only updates fiels provided in the request.
        """

        return Response({'method':"patch"})

    def delete(self, request, pk=None):
        """
        Delete and object.
        """

        return Response({'method':"delete"})



class HelloViewset(viewsets.ViewSet):
    """
    Test API ViewSet.
    """

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """
        Return a hello message.
        """

        a_viewset = [
            "uses actions (list, create, rerieve, update, partial_update)",
            "Automitically maps to URLs using Routers.",
            "provides more functionallity with less code."
        ]

        return Response({'message': "Hello", "a_viewset": a_viewset})

    def create(self, request):
        """
        Create a new hello message.
        """

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "Hello! {0}".format(name)

            return Response({'message': message})
    else:
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """
        Handles getting an object by its ID.
        """

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """
        Handles updating an object.
        """

        return Response({'http_method': "PUT"})

    def partial_update(self, request, pk=None):
        """
        Handles updating part of an object.
        """

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """
        Handles removing an object.
        """

        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Handles creating, and updating profiles.
    """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.object.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_field = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """
    Check email and password and return an auth token,
    """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        Use the ObtainAuthToken APIView to validate and create a token.
        """

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """
    Handles creating, reading and updating profile feed items.
    """

    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Sets the user profile to the logged in user.
        """
        serializer.save(user_profile=self.request.user)
