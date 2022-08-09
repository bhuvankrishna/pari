from django.db.models import Q
from django.views.generic import ListView
from wagtail.core.models import Site

from .models import painting


class paintingList(ListView):
    context_object_name = "paintings"

    def get_queryset(self):
        qs = painting.objects.live().raw(
            'SELECT DISTINCT ON (substr(district, 1, 1)) * '
            'FROM painting_painting JOIN location_location ON '
            'painting_painting.location_id=location_location.id '
            'JOIN wagtailcore_page ON wagtailcore_page.id=painting_painting.page_ptr_id '
            'ORDER BY substr(district, 1, 1), first_published_at DESC')
        return qs

    def get_context_data(self):
        context = super(paintingList, self).get_context_data()
        context["title"] = 'paintingS'
        context["sub_heading"] = 'People from every indian district'
        context["tab"] = 'gallery'
        context["current_page"] = 'painting-list'
        return context


class paintingDetail(ListView):
    context_object_name = "paintings"
    model = painting
    template_name = "painting/painting.html"

    def get_queryset(self):
        # TODO: Should return queryset instead of list
        # TODO: Improve query performance
        alphabet = self.kwargs['alphabet']
        paintings = painting.objects.live().filter(
            Q(location__district__istartswith=alphabet) | Q(image__locations__district__istartswith=alphabet)
        ).select_related('location', 'location__sub_district_type') \
            .prefetch_related('image__photographers', 'image__locations').distinct()
        paintings_with_matching_district_added = [self.with_matching_district(painting, alphabet) for painting in paintings]
        paintings_ordered_by_matching_district = sorted(paintings_with_matching_district_added,
                                                    key=lambda f: f.matching_district)
        return paintings_ordered_by_matching_district

    def get_context_data(self):
        context = super(paintingDetail, self).get_context_data()
        context["alphabet"] = self.kwargs["alphabet"]
        context["share_sub_heading"] = 'People from every Indian district'
        context['site'] = Site.find_for_request(self.request)
        context["slug"] = self.kwargs.get("slug")
        if context["slug"]:
            try:
                context["painting"] = next(painting for painting in self.get_queryset() if painting.slug == context["slug"])
            except StopIteration:
                pass
        context["current_page"] = 'painting-district'
        return context

    @staticmethod
    def with_matching_district(painting, alphabet):
        if painting.location.district.lower().startswith(alphabet.lower()):
            painting.matching_district = painting.location.district
            return painting

        painting_image_location = painting.image.locations.filter(district__istartswith=alphabet).first()
        painting.matching_district = painting_image_location and painting_image_location.district or ''
        return painting
