from wagtail.models import Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import InlinePanel
from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StreamBlock

from wagtail.admin.panels import FieldPanel
from django.db import models
from wagtail.models import Page
from django.core.validators import MinValueValidator, MaxValueValidator





from wagtail.blocks import StructBlock, TextBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.fields import StreamField

class CustomContentBlock(StructBlock):
    html = RawHTMLBlock(required=False, label="HTML код")
    css_class = CharBlock(required=False, label="CSS классы")
    style = TextBlock(required=False, label="Inline стили (CSS)")

    class Meta:
        label = "Кастомный блок контента"

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
        verbose_name="Кастомный HTML/CSS контент"
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("custom_content"),
    ]

    def __str__(self):
        return self.image.title






class Service(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255, verbose_name="Название", null=False)
    description = RichTextField(blank=True, verbose_name="Описание", null=True,)
    price = models.DecimalField(
        max_digits = 6, decimal_places=0, null=False, verbose_name="Цена",
    validators = [
        MinValueValidator(100),
        MaxValueValidator(100000),
    ],
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("price"),
    ]

    def __str__(self):
        return self.name


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


class DepartmentBlock(StructBlock):
    title = blocks.CharBlock(required=True, max_length=60, label="Название отделения")
    description = RichTextBlock(required=False, verbose_name="Описание отделения")
    images = StreamBlock(
        [("image", ImageChooserBlock(required=True))],
        verbose_name="Фотографии",
        required=False,
    )

    class Meta:
        icon = "folder"
        label = "Отделение"


class Promotion(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="promotions")
    title = models.CharField(max_length=255, verbose_name="Название", null=True)
    description = RichTextField(blank=True, verbose_name="Описание", null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Изображение",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.title


class HomePage(Page):
    body = RichTextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)

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
        InlinePanel("services", label="Услуги"),
        InlinePanel("faqs", label="Вопросы и ответы"),
        InlinePanel("carousel_images", label="Изображения карусели"),
        FieldPanel("departments"),
        InlinePanel("promotions", label="Акции"),
    ]


# TODO сделать динамический адрес через админку шрифт свести к одному названия на русском в админке влидацию в админке на цену на картинки акций итд и валидация блока с контактами  https://yandex.ru/dev/jsapi30/doc/ru/examples/cases/marker-popup    https://getbootstrap.com/docs/5.3/components/modal/
