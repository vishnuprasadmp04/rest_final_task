from django.shortcuts import render
from django.contrib.auth.models  import User
from rest_framework.response import Response
from api.models import *
from api.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authentication import BaseAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Create your views here.


class userViewset(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    
    
    def list(self, request, *args, **kwargs,):
        return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    def retrive(self, request,pk=0):
        return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    def destroy(self, request,pk=0):
        return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    
    
    
class ProductViewSet(ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    # def list(self, request):

    #     category = request.query_params.get("category")
    #     if category:
    #         products = Product.objects.filter(category=category)
    #     else:
    #         products = Product.objects.all()
    #     ser = ProductSerializer(products, many=True)

    #     return Response(ser.data)
    def get_queryset(self):
        qs=self.queryset
        if self.request.query_params:
            qs=qs.filter(category=self.request.query_params.get('category'))
        return qs
    def create(self, request):
            return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    def update(self, request,pk=0):
            return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    def partial_update(self, request,pk=0):
            return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    def destroy(self, request,pk=0):
            return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
        
    @action(methods=["POST"],detail=True)
    def addtocart(self,request,pk=0):
        user=request.user
        product=self.get_object()
        dser=CartSerializer(data=request.data)
        if dser.is_valid():
            dser.save(user=user,product=product)
            return Response(data=dser.data,status=status.HTTP_200_OK)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["POST"],detail=True)
    def addReview(self,request,pk=0):
        user=request.user
        product=self.get_object()
        dser=ReviewSerializer(data=request.data)
        if dser.is_valid():
            dser.save(user=user,product=product)
            return Response(data=dser.data,status=status.HTTP_200_OK)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class CartViewset(ModelViewSet):
    
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    serializer_class=CartSerializer
    queryset=Cart.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    def create(self, request,pk=0):
            return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    def update(self, request,pk=0):
            return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)
    def partial_update(self, request,pk=0):
            return Response(data={"msg":"Not allowed"},status=status.HTTP_403_FORBIDDEN)    
    @action(methods=["POST"],detail=True)
    def placeorder(self,request,pk=0):
        user=request.user
        product=self.get_object().product
        dser=Orderserializer(data=request.data)
        if dser.is_valid():
            dser.save(user=user,product=product)
            Cart.objects.get(id=self.get_object().id).delete()
            return Response(data=dser.data,status=status.HTTP_200_OK)
        return Response(data=dser.errors,status=status.HTTP_400_BAD_REQUEST)
            

class OrderViewset(ModelViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    def get_queryset(self):
        qs=self.queryset.filter(user=self.request.user)
        return qs
    def create(self, request):
        return Response(data={"msg":"Not Allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)
    def update(self, request):
        return Response(data={"msg":"Not Allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)
    def partial_update(self, request):
        return Response(data={"msg":"Not Allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)
    def destroy(self, request):
        return Response(data={"msg":"Not Allowed"},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    