from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import SellerSerializer, ProductSerializer, UserSerializer

from django.contrib.auth import authenticate, login, logout

from .models import Seller
from .models import Products

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token


# Create your views here.


@api_view(['POST', ])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    response = {}
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        response["token"] = token.key
        response["status"] = "success"
        return Response(response)
    return JsonResponse(serializer.errors, safe=False)


@api_view(['GET', 'POST', ])
@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    response = {}
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
        response["token"] = token.key
        response["status"] = "success"
        return Response(response)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']
        print('username', username)
        print('password', password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=request.user)
            response["token"] = token.key
            response["status"] = "success"
            return Response(response)
        else:
            response["token"] = "token"
            response["status"] = "failure"
            return Response(response)
    else:
        response["token"] = "token"
        response["status"] = "failure"
        return Response(response)


@api_view(['GET', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({
            "response": "success"
        })
    else:
        return Response({
            "response": "failure"
        })


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_products(request):
    # data = JSONParser().parse(request)
    print(request.data)
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "response": "success"
        })
    else:
        return Response({
            "response": "failure"
        })


@api_view(['GET', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_products(request):
    if request.user.is_authenticated:
        print("Authenticated")
    response = {}

    seller_id = request.user.username
    products = Products.objects.filter(seller_id=seller_id)
    if products:
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)
    response['status'] = "failure"
    return JsonResponse(response, safe=False)


@api_view(['PUT', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_products(request):
    product = Products.objects.get(pk=request.data['id'])
    if product:
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": "success"
            })
    return Response({
        "response": "failure"
    })


@api_view(['DELETE', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_products(request):
    print(request.data)
    product = Products.objects.get(pk=request.data['id'])
    if product:
        product.delete()
        return Response({
            "response": "success"
        })
    return Response({
        "response": "failure"
    })


@api_view(['GET', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_sellers(request):
    sellers = Seller.objects.all()
    serializer = SellerSerializer(sellers, many=True)
    return JsonResponse(serializer.data, safe=False)
