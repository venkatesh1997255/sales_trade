# Django Imports
from django.conf.urls import url

# Local Imports
from salesapp.views import BarCharts

urlpatterns = [
    url(r'bar_charts/$', BarCharts.as_view(), name="bar-charts")
]
