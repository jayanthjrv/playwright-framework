class AuthTokenGenerator:
    @staticmethod
    async def generate_auth_token(client):
        with open("APIAutomation/utils/core_token.txt", "r") as file:
            bearer_token = file.read().strip()
        response = await client.get('/api/auth/authorize', headers={'Content-Type': 'application/json',
                                                                    'Authorization': f'Bearer {bearer_token}'
                                                                    })
        return response.json()['token']
