import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse

from api.models import Team
from api.serializers import TeamSerializer
from api.tests.factories import CountryFactory
from api.tests.factories import LeagueFactory
from api.tests.factories import TeamFactory


User = get_user_model()


class TeamsAPITestCase(TestCase):
    _team_list_url = reverse("teams-list")

    def setUp(self) -> None:
        self.test_username = "test-user"
        self.test_password = "test-password"
        User.objects.create_user(
            username=self.test_username, password=self.test_password
        )
        self.country = CountryFactory(name="test-country")
        self.league1 = LeagueFactory()
        self.team1 = TeamFactory(league=self.league1, country=self.country)
        self.team2 = TeamFactory(league=self.league1)
        self.team3 = TeamFactory(name="abc blue team", country=self.country)
        self.team4 = TeamFactory(name="abc red team")

    def test_get_teams(self):
        response = self.client.get(self._team_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teams = Team.objects.all()
        serializer = TeamSerializer(data=teams, many=True)
        serializer.is_valid()
        data = serializer.data
        self.assertEqual(response.data, data)

    def test_get_teams_by_name(self):
        response = self.client.get(self._team_list_url, {"name": "abc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teams = [self.team3, self.team4]
        serializer = TeamSerializer(data=teams, many=True)
        serializer.is_valid()
        data = serializer.data
        self.assertEqual(response.data, data)

    def test_post_team_when_user_not_authenticated(self):
        data = {"name": "new-team"}
        response = self.client.post(self._team_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_team_validation(self):
        data = {}
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.post(
            self._team_list_url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_team(self):
        data = {
            "name": "new-team",
            "stadium_name": "test-stadium",
            "stadium_capacity": 123,
            "league": self.league1.id,
            "country": self.country.id,
            "year_founded": 2021,
        }
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.post(
            self._team_list_url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        team = Team.objects.get(**data)
        data.update(
            id=team.id, league_name=self.league1.name, country_name=self.country.name
        )
        self.assertEqual(response.data, data)

    def test_put_team(self):
        data = {
            "name": "new-team",
            "stadium_name": "test-stadium",
            "stadium_capacity": 123,
            "league": self.league1.id,
            "country": CountryFactory().id,
            "year_founded": 2021,
        }
        self.client.login(username=self.test_username, password=self.test_password)
        url = reverse("teams-detail", kwargs={"pk": self.team1.id})
        response = self.client.put(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data["id"] = self.team1.id
        self.assertEqual(Team.objects.filter(**data).count(), 1)

    def test_patch_team(self):
        data = {
            "name": "new-team",
            "stadium_name": "test-stadium",
        }
        self.client.login(username=self.test_username, password=self.test_password)
        url = reverse("teams-detail", kwargs={"pk": self.team1.id})
        response = self.client.patch(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data["id"] = self.team1.id
        self.assertEqual(Team.objects.filter(**data).count(), 1)

    def test_delete_team(self):
        self.client.login(username=self.test_username, password=self.test_password)
        url = reverse("teams-detail", kwargs={"pk": self.team1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.filter(id=self.team1.id).exists(), False)
