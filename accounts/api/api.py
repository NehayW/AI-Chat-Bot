from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer

# Chatbot
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_companion.views import load_chain, get_voicemessage
from ai_companion.models import ChatGptBot
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.GenericAPIView):
    """Registers users using email, username and password"""
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """Login API for user"""
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    """Logout API for user"""
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatbotResponse(APIView):
    """This API sends user input to a load chain function,
        which generates response from AI"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_input = request.data["user_input"]
            response = load_chain().predict(human_input=user_input)
            # get_voicemessage(response) # gets delayed because of voice messages
            ChatGptBot.objects.create(
                user=request.user,
                messageInput=user_input,
                bot_response=response,
            )
            context = {"response": response}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
