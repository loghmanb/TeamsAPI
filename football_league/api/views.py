from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Team
from api.serializers import TeamSerializer
from api.permissions import ReadOnly


class TeamViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing teams.
    """

    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_queryset(self):
        teams = Team.objects.all()
        name = self.request.query_params.get("name")
        if name:
            teams = teams.filter(name__icontains=name)
        country = self.request.query_params.get("country")
        if country:
            teams = teams.filter(league__country__name__icontains=country)
        return teams
