from rest_framework import routers
from views import App2ViewSet

router = routers.DefaultRouter()
router.register("app2", App2ViewSet)
urlpatterns = router.urls