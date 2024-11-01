from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import register_setting
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class Service(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("price"),
    ]

    def __str__(self):
        return self.name


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        InlinePanel("services", label="Услуги"),
    ]
