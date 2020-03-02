# Django Imports
from django.views.generic import TemplateView


class BarCharts(TemplateView):
    """
    Plot bar chart for the response
    Day name wise Turnover (Rs. Cr)'s average, minimum, maximum
    """
    template_name = "bar_chart.html"

