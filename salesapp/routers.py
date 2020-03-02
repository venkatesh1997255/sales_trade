# DRF Imports
from rest_framework import routers

# Local Imports
from salesapp.viewsets import TradedViewSet

router = routers.SimpleRouter()
router.register(r'trade', TradedViewSet, base_name="trade")
