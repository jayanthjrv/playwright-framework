import json
import os

import httpx
import pytest

from APIAutomation.utils.token_generator import AuthTokenGenerator


# @pytest.fixture
async def request(url, request_type, payload=''):
    async with httpx.AsyncClient(base_url=os.getenv("BASE_URL")) as client:
        auth_token = await AuthTokenGenerator.generate_auth_token(client)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }

        match request_type.lower():
            case 'get':
                response = await client.get(url, headers=headers)
            case 'post':
                response = await client.post(url, json=payload,headers=headers) if payload != '' else await client.post(url, headers=headers)
            case 'put':
                response = await client.put(url, json=payload, headers=headers) if payload != '' else await client.put(url, headers=headers)
            case 'patch':
                response = await client.patch(url, json=payload, headers=headers) if payload != '' else await client.patch(url, headers=headers)
            case 'delete':
                response = await client.delete(url, headers=headers)
            case _:
                raise ValueError("Invalid request type. Use 'get', 'post', 'put' or 'delete'.")
        return response
