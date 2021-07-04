from rest_framework import routers

from api.views import TeamViewSet

router = routers.SimpleRouter()
router.register(r"teams", TeamViewSet, "teams")


urlpatterns = router.urls
