from neomodel import StructuredNode, RelationshipTo, StructuredRel
from neomodel.contrib.spatial_properties import PointProperty
from neomodel.properties import BooleanProperty, StringProperty, UniqueIdProperty, DateProperty, \
    IntegerProperty, JSONProperty, DateTimeProperty


class User(StructuredNode):
    id = UniqueIdProperty()
    username = StringProperty()
    password = StringProperty()
    email = StringProperty()
    is_active = BooleanProperty()


class Territory(StructuredNode):
    id = IntegerProperty(unique_index=True)
    geometry = JSONProperty()


class ClaimedTerritoryRel(StructuredRel):
    date_start = DateTimeProperty()
    date_end = DateTimeProperty()


class Country(StructuredNode):
    id = IntegerProperty(unique_index=True)
    founded_at = DateProperty(required=False)
    dissolved_at = DateProperty(required=True, )
    name_zeit = StringProperty()
    name_eng = StringProperty()

    claims_territory = RelationshipTo(Territory, rel_type='TERRITORY', model=ClaimedTerritoryRel)


class PointOfInterest(StructuredNode):
    id = IntegerProperty(unique_index=True)
    # geometry = PointProperty(crs='')


class Population(StructuredNode):
    date_census = DateProperty()
    total = IntegerProperty()
    by_language = JSONProperty()
    by_faith = JSONProperty()
    by_political_affiliation = JSONProperty()
    by_gender = JSONProperty()
    approximations = JSONProperty()  # maps field names to the degree of certainty in them


class PersonOfInterest(StructuredNode):
    id = IntegerProperty(unique_index=True)
    name = StringProperty()
    born_at = DateProperty()
    deceased = DateProperty()


class DataSource(StructuredNode):
    id = IntegerProperty(unique_index=True)
    description = StringProperty()
    permalink = StringProperty()
