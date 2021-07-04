from django.db import models


class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]

    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class League(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=30, verbose_name="Team", blank=False, null=False)
    stadium_name = models.CharField(
        max_length=30, verbose_name="Stadium", blank=False, null=False
    )
    stadium_capacity = models.PositiveIntegerField(blank=False, null=False)
    league = models.ForeignKey(
        League, on_delete=models.SET_NULL, verbose_name="League", null=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=False
    )
    year_founded = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return self.name
