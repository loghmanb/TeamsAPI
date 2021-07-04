from rest_framework import serializers

from api.models import Team


class TeamSerializer(serializers.ModelSerializer):
    league_name = serializers.CharField(source="league.name", read_only=True)
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "stadium_name",
            "stadium_capacity",
            "league",
            "league_name",
            "country",
            "country_name",
            "year_founded",
        ]
        read_only_fields = ("league_name", "country_name")
