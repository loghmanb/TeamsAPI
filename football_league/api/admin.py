from django.contrib import admin

from api.models import Country
from api.models import League
from api.models import Team


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    list_display_links = ("name",)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "league", "country", "year_founded")
    list_display_links = ("id", "name")
    list_filter = ("country", "league")


admin.site.register(Country, CountryAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
