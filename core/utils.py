from __future__ import print_function
import datetime
from collections import OrderedDict
import re

from django.urls import reverse
from django.http import JsonResponse
from django.utils.translation import get_language, activate
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.rich_text import RichText


def get_translations_for_page(page):
    translations = []
    activate(get_language())

    try:
        trans_holder = page.get_children().get(title="Translations")
        if page.live:
            translations.append(page.specific)
        translations.extend(trans_holder.get_children().live().specific())
    except Page.DoesNotExist:
        # Check if page exists within the translation folder
        parent = page.get_parent()
        if parent.title == "Translations":
            if parent.get_parent().live:
                translations.append(parent.get_parent().specific)
            live_children = parent.get_children().live()
            if live_children:
                translations.extend(live_children.specific())
    return translations


def get_translated_or_default_page(default_page, translations):
    translated_page = default_page
    for translation in translations:
        if translation.language == get_language():
            translated_page = translation
    return translated_page


def filter_by_language(request, *items_to_filter):
    lang = get_language()
    filtered_list = []
    if request.GET.get("lang"):
        lang = request.GET["lang"]
    if not lang == 'all':
        for item in items_to_filter:
            filtered_list.append(item.filter(language=lang))
    return tuple(items_to_filter) if len(filtered_list) == 0 else tuple(filtered_list)


def get_translations_for_articles(articles):
    article_translations = {}
    for article in articles:
        article_translations[article] = get_translations_for_page(article)
    return article_translations


def get_unique_photographers(album):
    photographers = []
    for slide in album.slides.all():
        photographers.extend(slide.image.photographers.all())
    return set(photographers)


def get_slide_detail(album):
    response_data = {}
    response_data['slides'] = []
    photographers = []
    slide_photo_graphers = []
    for slide in album.slides.all():
        slide_photo_graphers.extend(map(lambda photographer_name: photographer_name.name,
                                        slide.image.photographers.all()))
    photographers_of_album = list(set(slide_photo_graphers))
    for index, slide in enumerate(album.slides.all(), start=0):
        slide_dict = dict([('type', 'image'), ('show_title', "True"), ('album_title', album.title)])
        slide_dict['src'] = slide.image.file.url
        slide_dict['src_resized'] = slide.image.get_rendition('height-876').url
        block = blocks.RichTextBlock()
        description_value = RichText(slide.description)
        slide_dict['description'] = block.render(description_value)
        slide_dict['album_description'] = album.description
        slide_dict['url'] = album.get_absolute_url()
        slide_dict['slide_photographer'] = list(map(lambda photographer_name: photographer_name.name,
                                               slide.image.photographers.all()))
        if index == 0:
            slide_dict['slide_photographer'] = photographers_of_album
        photographers.extend(set(slide.image.photographers.all()))
        if album.first_published_at:
            published_date = datetime.datetime.strptime(str(album.first_published_at)[:10], "%Y-%m-%d")
        else:
            published_date = datetime.datetime.now()
        date = published_date.strftime('%d %b,%Y')
        slide_dict['image_captured_date'] = date
        image_location = slide.image.locations.first()
        slide_dict['slide_location'] = "%s, %s" % (
        image_location.district, image_location.state) if image_location else ''
        slide_dict['track_id'] = slide.audio
        
        embed_value = RichText(slide.embed)
        embed_html = block.render(embed_value)
        embed_iframe = re.findall('https.*\?', embed_html)
        if (len(embed_iframe)>0):
        # if (len(embed_html)>0):
            slide_dict['embed'] = '<iframe src="' + embed_iframe[0] + 'showinfo=0&amp;modestbranding=1&amp;feature=oembed&amp;cc_load_policy=1&amp;autohide=1&amp;rel=0" allowfullscreen="" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" style="max-width: 1200px; position: absolute;left: 0;right: 0;top: 0;bottom: 0;margin: auto;" width="75%" height="100%"'
            # slide_dict['embed'] = embed_html
            slide_dict['carousel_html'] = slide_dict['embed']
        else: 
            slide_dict['embed'] = ""
            slide_dict['carousel_html'] = '<img src="'+ slide_dict['src_resized'] +'" />'

        response_data['slides'].append(slide_dict)

    response_data['authors'] = []
    for photographer in set(photographers):
        photographer_dict = dict(
            [('type', 'inline'), ('show_title', "False"), ('name', photographer.name), ('bio', photographer.bio_en),
             ('twitter_username', photographer.twitter_handle), ('facebook_username', photographer.facebook_username),
             ('email', photographer.email), ('website', photographer.website),
             ('author_url', reverse('author-detail', kwargs={'slug': photographer.slug}))])
        response_data['authors'].append(photographer_dict)
    return JsonResponse(response_data)


class SearchBoost(object):
    TITLE = 6
    AUTHOR = 5
    LOCATION = 4
    DESCRIPTION = 3
    CONTENT = 2


def construct_guidelines(guideline_content):
    guideline_dict = OrderedDict()
    for content in guideline_content:
        if content.block_type == "heading_title":
            current_heading = content.value
            guideline_dict[current_heading] = {"sub_section": []}
        if content.block_type == "heading_content":
            guideline_dict[current_heading]["heading_content"] = content.value
        if content.block_type == "sub_section_with_heading":
            guideline_dict[current_heading]["has_sub_section_with_heading"] = True
            guideline_dict[current_heading]["sub_section"].append(content.value)
        if content.block_type == "sub_section_without_heading":
            guideline_dict[current_heading]["has_sub_section_with_heading"] = False
            guideline_dict[current_heading]["sub_section"].append({"content": content.value})
    return guideline_dict
