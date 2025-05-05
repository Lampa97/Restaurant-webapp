from datetime import datetime

from celery import shared_task

from reservation.models import Reservation


@shared_task
def check_booking_status():
    """
    Check the status of each reservation and changing status to inactive when the reservation is over.
    """
    today_date = datetime.now().date()
    reservations = Reservation.objects.filter(is_active=True, date=today_date)
    for reservation in reservations:
        if reservation.end_time <= datetime.now().time():
            reservation.is_active = False
            reservation.save()
