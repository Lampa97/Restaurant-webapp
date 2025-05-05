from django.db.models import Sum

from .models import Review


def count_avg_rating():
    all_reviews = Review.objects.all()
    count_reviews = all_reviews.count()
    total_rating = all_reviews.aggregate(Sum("rating"))["rating__sum"]
    if count_reviews == 0:
        avg_rating = 0
    else:
        avg_rating = total_rating / count_reviews
    return avg_rating
