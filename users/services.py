from django.utils.timezone import now

from reservation.models import Reservation


def get_closest_booking_date(user):
    # Fetch the closest reservation date for the user
    closest_reservation = Reservation.objects.filter(user=user, date__gte=now().date()).order_by("date").first()
    return closest_reservation.date if closest_reservation else None
