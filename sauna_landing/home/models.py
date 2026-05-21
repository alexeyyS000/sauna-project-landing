from wagtail.models import Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import InlinePanel
from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.admin.panels import FieldPanel
from django.db import models
from wagtail.models import Page


from wagtail.blocks import (
    StructBlock,
    RichTextBlock,
    RawHTMLBlock,
)
from wagtail.fields import StreamField
from home.utils.witgets import CodeMirrorPanel

class CustomContentBlock(StructBlock):
    html = RawHTMLBlock(required=False, label="HTML код")


    class Meta:
        label = "Кастомный блок контента"

    panels = [FieldPanel("html", widget=CodeMirrorPanel)]


class CarouselImage(Orderable):
    page = ParentalKey(
        "HomePage", on_delete=models.CASCADE, related_name="carousel_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Картинка для карусели",
    )
    custom_content = StreamField(
        [("custom_block", CustomContentBlock())],
        blank=True,
        verbose_name="Кастомный HTML/CSS контент",
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("custom_content"),
    ]

    def __str__(self):
        return self.image.title




class FAQ(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255, verbose_name="Вопрос", null=False)
    answer = RichTextField(blank=True, verbose_name="Ответ", null=False)

    panels = [
        FieldPanel("question"),
        FieldPanel("answer"),
    ]

    def __str__(self):
        return self.question


class PriceItemBlock(StructBlock):
    name = blocks.CharBlock(required=True, label="Услуга")
    price = blocks.DecimalBlock(    required=True,
    label="Цена",
    max_digits=6,
    decimal_places=0,
    min_value=100,
    max_value=100000,)
    description = blocks.RichTextBlock(required=False, label="Описание")

    class Meta:
        icon = "tag"

class DepartmentBlock(StructBlock):
    title = blocks.CharBlock(required=True, max_length=60, label="Название отделения")
    description = RichTextBlock(required=False, verbose_name="Описание отделения")
    disabled = blocks.BooleanBlock(required=False, label="Отключить отделение", default=False)
    images = blocks.StreamBlock(
        [("image", ImageChooserBlock(required=True))],
        verbose_name="Фотографии",
        required=False,
    )
    # Режим работы: список записей (день недели + описание/часы)
    working_hours = blocks.ListBlock(
        StructBlock(
            [
                ("day", blocks.CharBlock(required=True, max_length=20, label="День недели")),
                ("info", blocks.CharBlock(required=False, max_length=30, label="Описание / часы")),
            ],
            label="День режима работы",
            icon="time",
        ),
        required=False,
        label="Режим работы",
    )
    pricelist = blocks.ListBlock(
        PriceItemBlock(),
        required=False,
        label="Прайскурант",
    )

    class Meta:
        icon = "folder"
        label = "Отделение"


class Promotion(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="promotions")
    title = models.CharField(max_length=255, verbose_name="Название", null=True)
    description = RichTextField(blank=True, verbose_name="Описание", null=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


# New Phone model: stores a phone number and its label/name and links to HomePage
class Phone(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="phones")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
    number = models.CharField(max_length=50, verbose_name="Номер телефона")

    panels = [
        FieldPanel("title"),
        FieldPanel("number"),
    ]

class HomePage(Page):

    body = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Заголовок"
    )
    description = RichTextField(blank=True, null=True)

    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Адрес"
    )
    departments = StreamField(
        [
            ("department", DepartmentBlock(required=False)),
        ],
        verbose_name="Отделения сауны",
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("description"),
        InlinePanel("carousel_images", label="Изображения карусели"),
        FieldPanel("departments"),
        FieldPanel("address"),
        # InlinePanel for phones so editors can add multiple phone numbers per HomePage
        InlinePanel("promotions", label="Акции"),
        InlinePanel("faqs", label="Вопросы и ответы"),
        InlinePanel("phones", label="Телефоны"),
    ]
