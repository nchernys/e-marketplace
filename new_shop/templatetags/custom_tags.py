from django import template
from django.db.models import Count, Sum

register = template.Library()

def count_stats(r, t): 
    summary = sum(r.quantity for r in t)
    return summary

register.filter('count_stats', count_stats)