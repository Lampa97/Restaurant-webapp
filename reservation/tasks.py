import logging
from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from reservation.models import Reservation

logger = logging.getLogger(__name__)


@shared_task
def check_booking_status():
    """
    Task to deactivate expired reservations.

    Deactivates reservations where the end time has passed and the reservation is still active.
    """
    today_date = datetime.now().date()
    reservations = Reservation.objects.filter(is_active=True, date__lte=today_date)
    for reservation in reservations:
        if reservation.end_time <= datetime.now().time() or reservation.date < today_date:
            reservation.is_active = False
            reservation.save()


@shared_task
def send_notification_email():
    """
    Send a notification email to the user about upcoming reservation time.
    """
    logger.info("Task started")
    now = datetime.now()
    reservations = Reservation.objects.filter(is_active=True, date=now.date(), start_time__gt=now.time())
    logger.info(reservations)
    for reservation in reservations:
        logger.info(reservation)
        if reservation.user.email:
            # Combine date and time into datetime objects
            reservation_time = datetime.combine(reservation.date, reservation.start_time)
            now_time = datetime.combine(reservation.date, now.time())

            # Calculate the time difference
            time_difference = reservation_time - now_time
            logger.info(time_difference)
            if timedelta(minutes=59) <= time_difference <= timedelta(hours=2, minutes=1):
                subject = "Upcoming Reservation Reminder"
                message = (
                    f"Dear {reservation.user},\n\nYour reservation at Iron Hoof SteakHouse is coming up soon!\n\n"
                    f"Date: {reservation.date}\n"
                    f"Time: {reservation.start_time} - {reservation.end_time}\n\n"
                    f"Table № {reservation.table.number}\n"
                    f"Total persons: {reservation.total_persons}\n"
                    f"Thank you for using our service!"
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reservation.user.email],
                )
