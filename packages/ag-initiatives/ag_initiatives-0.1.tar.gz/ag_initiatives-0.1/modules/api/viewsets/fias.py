import requests
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class FIASViewset(ViewSet):
    gar_url = 'http://gar-service:8000'

    def post_to_api(self, url, data):
        try:
            response = requests.post(url, json=data, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": e}

    @action(detail=False, methods=['post'])
    def full_addresses(self, request):
        data = request.data
        full_addresses_response = self.post_to_api(f"{self.gar_url}/api/gar/full_addresses/", data)
        return Response(full_addresses_response)

    @action(detail=False, methods=['post'])
    def forward(self, request):
        data = request.data
        forward_response = self.post_to_api(f"{self.gar_url}/api/gar/forward/", data)
        return Response(forward_response)

    @action(detail=False, methods=['post'])
    def reverse(self, request):
        data = request.data
        reverse_response = self.post_to_api(f"{self.gar_url}/api/gar/reverse/", data)
        return Response(reverse_response)
