from .models import NFT
from rest_framework import serializers
from .models import UserProfile



class WalletAddressSerializer(serializers.Serializer):
    walletAddress = serializers.CharField()


class VerifySignatureSerializer(serializers.Serializer):
    walletAddress = serializers.CharField()
    signature = serializers.CharField()
    hash = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = '__all__'



class NFTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = '__all__'