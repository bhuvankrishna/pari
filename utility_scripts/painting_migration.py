from __future__ import print_function
import csv
from datetime import datetime

import django
from django.utils.text import slugify

from author.models import Author
from location.models import Location
from location.models import SubDistrictType
from painting.models import painting
from core.models import AffixImage

django.setup()

with open('updated_paintings_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        # Painting data
        painting_image_id = row['id']
        name, occupation, occupation_of_parent = row['name'], row['occupation'], row['occupation of parent']
        age, is_a_child = row['age'], row['is_a_child']
        gender, quote = row['gender'], row['quote']
        adivasi = row['adivasi']
        additional_info = row['additional info']

        # Painting image data
        camera, date, photographer = row['camera'], row['date'], row['photographer']

        # Location data
        location_name, location_district, location_state = row['village'], row['district'], row['state']
        region, panchayat = row['region'], row['panchayat']
        subdistrict_name = row['mandal'] or row['mandapam'] or row['taluka'] or row['tehsil'] or row['block']
        subdistrict_type = (row['mandal'] and 'mandal') or (row['mandapam'] and 'mandapam') \
                           or (row['taluka'] and 'taluka') or (row['tehsil'] and 'tehsil') or (row['block'] and 'block')

        subdistrict_type = subdistrict_name and subdistrict_type and SubDistrictType.objects.get(name=subdistrict_type)

        painting = Painting.objects.get(image_id=painting_image_id)
        painting_image = AffixImage.objects.get(pk=painting_image_id)
        painting_location = Location.objects.get(pk=painting.location_id)
        location_name = location_name or painting_location.name

        if painting.has_unpublished_changes and painting.first_published_at is not None:
            painting.revisions.all().delete()
        if painting.has_unpublished_changes and painting.first_published_at is None:
            painting.revisions.all().delete()

        print()
        print("location_name: " + location_name)
        print("subdistrict_name: " + subdistrict_name)
        print("subdistrict_type: " + (subdistrict_type and subdistrict_type.name))

        new_location, created = Location.objects.get_or_create(
            name=location_name,
            district=location_district,
            state=location_state,
            point=painting.location.point,
            sub_district_name=subdistrict_name or None,
            sub_district_type_id=(subdistrict_type and subdistrict_type.id) or None,
            region=region or None,
            panchayat=panchayat or None
        )

        print("Painting id: %s" % painting.id)
        print("Painting image id: %s" % painting.image_id)
        print("New location %s, %s" % (new_location.name, created))
        print("Current location ID: %s" % painting.location_id)
        print("Newlocation ID: %s" % new_location.id)

        painting.location_id = new_location.id

        if name:
            painting.name = name
        if occupation:
            painting.occupation = occupation
        if occupation_of_parent:
            painting.occupation_of_parent = occupation_of_parent
        if age:
            painting.age = age
        if is_a_child:
            painting.child = True if is_a_child.lower() == 'yes' else False
        if gender:
            if gender.lower() == 'female':
                painting.gender = 'F'
            elif gender.lower() == 'male':
                painting.gender = 'M'
            elif gender.lower() == 'transgender':
                painting.gender = 'T'
            else:
                raise Exception('Non matching gender for painting id: %s' % painting.id)
        if quote:
            painting.quote = quote
        if adivasi:
            painting.adivasi = adivasi

        painting.additional_info = additional_info

        painting.save()

        new_location.slug = slugify(name)[:50]
        new_location.save()

        if camera:
            painting_image.camera = camera
        if date:
            painting_image.date = datetime.strptime(date, '%B %d, %Y')
        painting_image.save()

        if photographer:
            new_photographer, created = Author.objects.get_or_create(name=photographer)
            new_photographer.slug = slugify(photographer)
            new_photographer.save()
            painting_image.photographers.add(new_photographer)

        updated_painting = Painting.objects.get(image_id=painting_image_id)
        print("updated ID: %s" % updated_painting.location_id)

        print("Current Painting image locations: %s" % ",".join([each.name for each in painting_image.locations.all()]))
        painting_image.locations.clear()

        painting_image_locations_after_clear = AffixImage.objects.get(pk=painting_image_id).locations
        print("After clear painting image locations: %s" % ",".join(
            [each.name for each in painting_image_locations_after_clear.all()]))

        painting_image_locations_after_clear.add(new_location)

        painting_image_locations_after_update = AffixImage.objects.get(pk=painting_image_id).locations
        print("After update painting image locations: %s" % ",".join(
            [each.name for each in painting_image_locations_after_update.all()]))
