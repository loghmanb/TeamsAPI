import factory
from factory.django import DjangoModelFactory

from api.models import Country
from api.models import League
from api.models import Team


class CountryFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Country-{n}")

    class Meta:
        model = Country


class LeagueFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Team-{n}")

    class Meta:
        model = League


class TeamFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Team-{n}")
    stadium_name = factory.Sequence(lambda n: f"Stadium-{n}")
    stadium_capacity = factory.Sequence(lambda n: n)
    league = factory.SubFactory(LeagueFactory)
    country = factory.SubFactory(CountryFactory)
    year_founded = factory.Sequence(lambda n: n)

    class Meta:
        model = Team
