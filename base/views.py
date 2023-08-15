from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import hashlib

import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import UserProfile
import json
from django.http import JsonResponse
from web3 import Web3
import time
import requests
from eth_account.messages import encode_defunct
from .serializers import VerifySignatureSerializer

from django_ratelimit.decorators import ratelimit

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from django.http import JsonResponse



def base(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render())



@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def nft_list(request):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token = authorization_header.split(' ')[1]  

        user_profile = UserProfile.objects.get(access_token=token)
        if(user_profile):
            data = [
                {
                    "name": "NFT 1",
                    "image_url": "https://source.unsplash.com/random/?nft",
                    "description": "Description of NFT 1"
                },
                {
                    "name": "NFT 2",
                    "image_url": "https://source.unsplash.com/random/?car",
                    "description": "Description of NFT 2"
                },
                {
                    "name": "NFT 3",
                    "image_url": "https://source.unsplash.com/random/?apple",
                    "description": "Description of NFT 3"
                },
                {
                    "name": "NFT 4",
                    "image_url": "https://source.unsplash.com/random/?mango",
                    "description": "Description of NFT 4"
                },
                {
                    "name": "NFT 5",
                    "image_url": "https://source.unsplash.com/random/?tea",
                    "description": "Description of NFT 5"
                },
                {
                    "name": "NFT 6",
                    "image_url": "https://source.unsplash.com/random/?oranges",
                    "description": "Description of NFT 6"
                },
                {
                    "name": "NFT 7",
                    "image_url": "https://source.unsplash.com/random/?cherry",
                    "description": "Description of NFT 7"
                },
                {
                    "name": "NFT 8",
                    "image_url": "https://source.unsplash.com/random/?kabul",
                    "description": "Description of NFT 8"
                },
                {
                    "name": "NFT 9",
                    "image_url": "https://source.unsplash.com/random/?angel",
                    "description": "Description of NFT 9"
                },
                {
                    "name": "NFT 10",
                    "image_url": "https://source.unsplash.com/random/?sana",
                    "description": "Description of NFT 10"
                }
            ]

            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({"Error":"Invalid Token"}, safe=False, status=status.HTTP_401_UNAUTHORIZED)
        
    return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)



@ratelimit(key='ip', rate='3/m', block=True)
@api_view(['POST'])
def generate_challenge(request):
    if request.method == 'POST':
        wallet_address = request.data.get('walletAddress')
        user_profile, created = UserProfile.objects.get_or_create(
            wallet_address=wallet_address)

        if not created and user_profile.challenge_expiration and user_profile.challenge_expiration >= int(time.time()):
            combined_string = f"{int(time.time())}-{hashlib.sha256(str(wallet_address).encode()).hexdigest()}"
            challenge_hash = hashlib.sha256(
                combined_string.encode()).hexdigest()

            current_unix_time = int(time.time())
            expiration = current_unix_time + 300

            user_profile.challenge = challenge_hash
            user_profile.challenge_expiration = expiration
            user_profile.save()
            response_data = {
                'challenge': user_profile.challenge,
                'expiration': user_profile.challenge_expiration
            }
            print(challenge_hash,"Challenge Hash Retrieved")

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            combined_string = f"{int(time.time())}-{hashlib.sha256(str(wallet_address).encode()).hexdigest()}"
            challenge_hash = hashlib.sha256(
                combined_string.encode()).hexdigest()

            current_unix_time = int(time.time())
            expiration = current_unix_time + 300

            user_profile.challenge = challenge_hash
            user_profile.challenge_expiration = expiration
            user_profile.save()

            response_data = {
                'challenge': challenge_hash,
                'expiration': expiration
            }

            print(challenge_hash,"Challenge Hash Generated")
            return JsonResponse(response_data, status=status.HTTP_200_OK)
    return JsonResponse({"Error":"Too Many Requests"}, status=status.HTTP_429_TOO_MANY_REQUESTS)


@api_view(['POST'])
def verify_signature(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        
        serializer = VerifySignatureSerializer(data=data)
        if serializer.is_valid():
            wallet_address = serializer.validated_data['walletAddress']
            signature = serializer.validated_data['signature']
            hash_value = serializer.validated_data['hash']

            try:
                user_profile = UserProfile.objects.get(
                    wallet_address=wallet_address)
                
                if  user_profile.challenge and user_profile.challenge_expiration >= int(time.time()):
                    w3 = Web3(Web3.HTTPProvider(
                        'https://mainnet.infura.io/v3/06c5ecfac7ff45179b8ba1d3b739bf88'))
                    message = encode_defunct(text=hash_value)
                    
                    verified = (w3.eth.account.recover_message(
                        message, signature=signature)).lower() == wallet_address

                    print(verified,"Signature Verification Status")
                    if verified:
                        token_url = 'http://127.0.0.1:8000/api/token/'
                        response = requests.post(
                            token_url, data={'username': 'admin', 'password': '123456'})

                        if response.status_code == status.HTTP_200_OK:
                            token_data = response.json()

                            if 'access' in token_data:
                                access_token = token_data['access']
                                user_profile.access_token = access_token 
                                user_profile.save()
                                print(access_token,"Access Token Generated")
                                return JsonResponse({'access_token': access_token}, status=status.HTTP_200_OK)
                            else:
                                return JsonResponse({'detail': 'Access token not found'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return JsonResponse({'detail': 'Failed to obtain token'}, status=response.status_code)
                    else:
                        return JsonResponse({'detail': 'Signature verification failed'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'detail': 'Expired challenge or challenge not found'}, status=status.HTTP_400_BAD_REQUEST)
            except UserProfile.DoesNotExist:
                return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
