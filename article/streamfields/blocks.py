from functools import partial

from django import forms
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from wagtail.core import blocks
from wagtail.core.blocks import PageChooserBlock, RichTextBlock, FieldBlock, RawHTMLBlock, IntegerBlock
from wagtail.core.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from album.models import Album
from core.widgets import JqueryChosenSelectMultipleWithAddObject
from face.models import Face
from painting.models import painting
from location.models import Location
from resources.models import Resource
import operator

ALIGNMENT_CHOICES = [('left', 'Left column'), ('right', 'Right column')]

RichTextMiniBlock = partial(RichTextBlock, features=['bold', 'italic'])
RichTextParagraphBlock = partial(RichTextBlock,
                                 features=['h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link',
                                           'document-link'])


class ModelMultipleChoiceBlock(FieldBlock):
    def __init__(self, target_model, required=True, help_text=None, **kwargs):
        self.target_model = target_model
        self.field = forms.ModelMultipleChoiceField(
            queryset=self.target_model.objects.all(),
            widget=JqueryChosenSelectMultipleWithAddObject,
            required=required,
            help_text=help_text,
        )
        super(ModelMultipleChoiceBlock, self).__init__(**kwargs)

    def to_python(self, value):
        if not value:
            return value
        else:
            return self.target_model.objects.filter(pk__in=value)

    def get_prep_value(self, value):
        if not value:
            return value
        else:
            return [each.pk for each in value]

    def value_from_form(self, value):
        if not value or all(isinstance(each, self.target_model) for each in value):
            return value
        else:
            return self.target_model.objects.filter(pk__in=value)

    def value_for_form(self, value):
        if not value:
            return value
        elif all(isinstance(each, self.target_model) for each in value):
            return [each.pk for each in value]
        else:
            return []


# TODO implement caption in the block it is implemented in.
class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    class Meta:
        icon = 'image'
        template = 'article/blocks/image.html'


# TODO: This is implemented in the latest wagtail. Remove it after upgrading.
class PageTypeChooserBlock(PageChooserBlock):
    """Custom implementation of PageChooserBlock to limit page selection to specific page types.
    """

    def __init__(self, for_models=[Page], **kwargs):
        self.for_models = for_models
        super(PageTypeChooserBlock, self).__init__(**kwargs)

    @cached_property
    def target_model(self):
        if len(self.for_models) == 1:
            return self.for_models[0]
        else:
            from wagtail.core.models import Page
            return Page

    @cached_property
    def widget(self):
        from django.utils.translation import ugettext_lazy as _
        from wagtail.admin.widgets import AdminPageChooser

        # Support importing from dotted string in-order to prevent circular-import for certain models(Say Article)
        self.for_models = [import_string(model) if isinstance(model, str) else model for model in self.for_models]
        if any(not issubclass(each, Page) for each in self.for_models):
            raise TypeError("All models passed should be a sub-class of wagtail.core.models.Page")

        model_names = ' / '.join(each.__name__.lower() for each in self.for_models)
        admin_page_chooser = AdminPageChooser(target_models=self.for_models)
        admin_page_chooser.choose_one_text = _('Choose a %s' % model_names)
        admin_page_chooser.choose_another_text = _('Choose another %s' % model_names)
        admin_page_chooser.link_to_chosen_text = _('Edit this %s' % model_names)
        return admin_page_chooser


class FullWidthImageBlock(blocks.StructBlock):
    image = ImageBlock()
    caption = RichTextMiniBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'article/blocks/full_width_image.html'
        label = 'Full width image'


class TwoColumnImageBlock(blocks.StructBlock):
    image_left = ImageBlock()
    image_right = ImageBlock()

    class Meta:
        icon = 'image'
        template = 'article/blocks/two_column_image.html'


class ParagraphBlock(blocks.StructBlock):
    ALIGN_CONTENT_CHOICES = [('default', 'Default'), ('center', 'Center')]
    content = RichTextParagraphBlock()
    align_content = blocks.ChoiceBlock(choices=ALIGN_CONTENT_CHOICES, default=ALIGN_CONTENT_CHOICES[0][0])

    class Meta:
        icon = 'title'
        label = 'Text'
        template = 'article/blocks/paragraph.html'


class PargraphBlockWithOptionalContent(ParagraphBlock):
    content = RichTextParagraphBlock(required=False)


class ParagraphWithImageBlock(blocks.StructBlock):
    image = ImageBlock()
    align_image = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])
    content = ParagraphBlock()

    class Meta:
        icon = 'doc-full'
        label = 'Paragraphs with an image'
        template = 'article/blocks/paragraph_with_image.html'


class FaceBlock(blocks.StructBlock):
    face = PageTypeChooserBlock(for_models=[Face])

    class Meta:
        icon = 'image'
        template = 'article/blocks/face.html'

class paintingBlock(blocks.StructBlock):
    painting = PageTypeChooserBlock(for_models=[painting])

    class Meta:
        icon = 'image'
        template = 'article/blocks/painting.html'


class ParagraphWithBlockQuoteBlock(blocks.StructBlock):
    quote = RichTextMiniBlock()
    align_quote = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[1][0])
    content = ParagraphBlock()

    class Meta:
        icon = 'openquote'
        label = 'Quote with text'
        template = 'article/blocks/paragraph_with_block_quote.html'


class FullWidthBlockQuote(blocks.StructBlock):
    quote = RichTextMiniBlock()

    class Meta:
        icon = 'openquote'
        label = 'Full width quote'
        template = 'article/blocks/full_width_block_quote.html'


class NColumnParagraphBlock(blocks.StructBlock):
    paragraph = blocks.ListBlock(ParagraphBlock())

    class Meta:
        template = 'article/blocks/columnar_paragraph.html'
        label = 'Columnar text'
        icon = 'title'


class ParagraphWithEmbedBlock(blocks.StructBlock):
    embed = EmbedBlock()
    embed_caption = RichTextMiniBlock(required=False)
    embed_max_width = IntegerBlock(required=False, help_text="Optional field. Maximum width of the content in pixels to"
                                                             " be requested from the content provider(e.g YouTube). "
                                                             "If the requested width is not supported, provider will be"
                                                             " supplying the content with nearest available width.")
    embed_align = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])
    content = ParagraphBlock()

    class Meta:
        icon = 'media'
        label = 'Embed with text'
        template = 'article/blocks/paragraph_with_embed.html'


class NColumnImageBlock(blocks.StructBlock):
    images = blocks.ListBlock(ImageBlock())
    height = IntegerBlock(min_value=0, required=True, default=380)
    caption = RichTextMiniBlock(required=False)

    class Meta:
        template = 'article/blocks/columnar_image.html'
        label = 'Columnar Images'


class ParagraphWithRawEmbedBlock(blocks.StructBlock):
    embed = RawHTMLBlock(help_text="Embed HTML code(an iframe)")
    embed_caption = RichTextMiniBlock(required=False)
    embed_align = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])
    content = PargraphBlockWithOptionalContent(required=False)

    class Meta:
        icon = 'media'
        label = 'Raw embed with text'
        template = 'article/blocks/paragraph_with_raw_embed.html'


class FullWidthEmbedBlock(blocks.StructBlock):
    embed = EmbedBlock(required=True, help_text="Enter URL for the embed block")
    embed_caption = RichTextMiniBlock(required=False)

    class Meta:
        icon = 'media'
        label = 'Full width embed'
        template = 'article/blocks/full_width_embed.html'


class VideoWithQuoteBlock(blocks.StructBlock):
    video = EmbedBlock(help_text="YouTube video URL")
    video_height = IntegerBlock(required=True, default=270)
    video_caption = RichTextMiniBlock(required=False)
    quote = RichTextMiniBlock()
    align_quote = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][1])

    class Meta:
        icon = 'openquote'
        label = 'Video with quote'
        template = 'article/blocks/video_with_block_quote.html'

class ParagraphWithMapBlock(blocks.StructBlock):
    locations = ModelMultipleChoiceBlock(target_model=Location)
    map_align = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])
    content = ParagraphBlock()

    class Meta:
        label = 'Map with text'
        template = 'article/blocks/paragraph_with_map.html'
        icon = 'site'


class ImageWithCaptionAndHeightBlock(ImageBlock):
    height = IntegerBlock(min_value=0, required=True, default=380)
    caption = RichTextMiniBlock(required=False)


class ImageWithQuoteAndParagraphBlock(blocks.StructBlock):
    image = ImageWithCaptionAndHeightBlock(required=True)
    align_image = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])
    content_1 = PargraphBlockWithOptionalContent(required=False)
    quote = FullWidthBlockQuote(required=True)
    content_2 = PargraphBlockWithOptionalContent(required=False)

    class Meta:
        icon = "image"
        label = 'Image with quote and text'
        template = 'article/blocks/image_with_quote_and_paragraph.html'


# TODO remove this class , this module is deprecated.
class ImageWithBlockQuote(blocks.StructBlock):
    image = ImageWithCaptionAndHeightBlock()
    quote = RichTextMiniBlock()
    align_quote = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])

    class Meta:
        icon = 'image'
        template = 'article/blocks/image_with_block_quote.html'
        label = 'Image with block quote'


class ParagraphWithPageBlock(blocks.StructBlock):
    page = PageTypeChooserBlock(for_models=['article.models.Article', Album, Face, painting, Resource])
    align_image = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])
    content = ParagraphBlock()

    class Meta:
        icon = 'link'
        template = 'article/blocks/paragraph_with_page.html'
        label = 'Page reference with text'


class NColumnImageWithTextBlock(NColumnImageBlock):
    align_columnar_images = blocks.ChoiceBlock(choices=ALIGNMENT_CHOICES, default=ALIGNMENT_CHOICES[0][0])
    content = PargraphBlockWithOptionalContent(required=False)

    class Meta:
        icon = 'image'
        label = 'Columnar images with text'
