from django import template

register = template.Library()


@register.filter(name='alt_text')
def alt_text(painting):
    return u'{name} is a {occupation} from {location}'.format(name=painting.title, occupation=painting.occupation or 'person',
                                                             location=painting.location or 'India')

