from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock, StreamBlock, RichTextBlock
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from django.db import models
from wagtail.models import Page


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

    class FAQ(Orderable):
        page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="faqs")
        question = models.CharField(max_length=255)
        answer = RichTextField(blank=True)

        panels = [
            FieldPanel("question"),
            FieldPanel("answer"),
        ]

        def __str__(self):
            return self.question


class DepartmentBlock(StructBlock):
    title = blocks.CharBlock(required=True, max_length=60, label="Название отделения")
    description = RichTextBlock(required=False, verbose_name="Описание отделения")
    images = StreamBlock(
        [("image", ImageChooserBlock(required=True))],
        verbose_name="Фотографии",
        required=False,
    )

    class Meta:
        # template = "blocks/sauna_department_block.html"
        icon = "folder"
        label = "Отделение"


class Promotion(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="promotions")
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.title


class HomePage(Page):
    body = RichTextField(blank=True)

    departments = StreamField(
        [
            ("department", DepartmentBlock(required=False)),
        ],
        verbose_name="Отделения сауны",
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        InlinePanel("services", label="Услуги"),
        InlinePanel("faqs", label="Вопросы и ответы"),
        FieldPanel("departments"),
        InlinePanel("promotions", label="Акции"),
    ]
