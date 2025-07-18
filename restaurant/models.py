from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Service Name")
    description = models.TextField(verbose_name="Service Description")
    image = models.ImageField(upload_to="services/", verbose_name="Service Image")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["name"]
        permissions = [
            ("can_admin_website", "Can administer the website"),
        ]

    def __str__(self):
        return self.name


class Personnel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Personnel Name")
    position = models.CharField(max_length=100, verbose_name="Personnel Position")
    description = models.TextField(verbose_name="Personnel Description")
    quote = models.TextField(verbose_name="Personnel Quote")
    photo = models.ImageField(upload_to="personnel/", verbose_name="Personnel Photo", default="default_person.jpg")

    class Meta:
        verbose_name = "Personnel"
        verbose_name_plural = "Personnel"
        ordering = ["name"]
        unique_together = ("name", "position")
        permissions = [
            ("can_admin_website", "Can administer the website"),
        ]

    def __str__(self):
        return f"{self.name} - {self.position}"


class Review(models.Model):

    name = models.CharField(max_length=100, verbose_name="Reviewer Name")
    review_text = models.TextField(verbose_name="Review Text")
    rating = models.PositiveSmallIntegerField(
        verbose_name="Rating",
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Review Date")

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-date"]
        permissions = [
            ("can_admin_website", "Can administer the website"),
        ]

    def __str__(self):
        return f"{self.name} - {self.rating}"
