from celery import shared_task
from datetime import datetime
from reservation.models import Reservation

@shared_task
def check_booking_status():
    """
    Check the status of each reservation and changing status to inactive when the reservation is over.
    """
    reservations = Reservation.objects.filter(is_active=True)
    for reservation in reservations:
        if reservation.date <= datetime.now().date() and reservation.end_time <= datetime.now().time():
            reservation.is_active = False
            reservation.save()