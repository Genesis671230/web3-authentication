from eth_account.messages import encode_defunct

from web3 import Web3

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import UserProfile
from django.utils import timezone
from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from mixer.backend.django import mixer
import json
from unittest.mock import patch
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils import timezone

class TestGenerateChallengeAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.generate_challenge_url = reverse('generate-challenge')
        self.existing_wallet_address = '0x8d35067233605bef6069191ae0922d134ff80d48'
        self.non_existing_wallet_address = '0x8d35067233605bef6069191ae0922d134ff80d49'
        self.existing_wallet_user = UserProfile.objects.create(wallet_address=self.existing_wallet_address)
        print(self.generate_challenge_url)

    def test_generate_challenge_new_wallet(self):
        response = self.client.post(self.generate_challenge_url, {'walletAddress': self.non_existing_wallet_address})
        db_data = UserProfile.objects.get(wallet_address=self.non_existing_wallet_address)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['challenge'], db_data.challenge)

  
