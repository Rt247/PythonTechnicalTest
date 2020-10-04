from rest_framework.views import APIView
from rest_framework.response import Response

class BondsListView(APIView):
    """
        View to ingest and query bond data
    """
    def get(self, request):
        return Response("Get Bonds!")

    def post(self, request):
        return Response("Post Bonds!")
