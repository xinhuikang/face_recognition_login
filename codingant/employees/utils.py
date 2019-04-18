from datetime import timedelta

from django.utils import timezone


def calculate_age(calculate_date, birth_date):
    return (calculate_date - birth_date).days // 365
