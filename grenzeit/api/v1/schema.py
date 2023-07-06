from neomodel import StructuredNode, RelationshipTo, StructuredRel
from neomodel.properties import BooleanProperty, StringProperty, UniqueIdProperty, DateProperty, \
    JSONProperty, DateTimeProperty


class User(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty()
    password = StringProperty()
    email = StringProperty()
    is_active = BooleanProperty()


class Territory(StructuredNode):
    uid = UniqueIdProperty()
    geometry = JSONProperty()


class ClaimedTerritoryRel(StructuredRel):
    date_start = DateProperty()
    date_end = DateProperty(required=False)


class Country(StructuredNode):
    uid = UniqueIdProperty()
    name_eng = StringProperty()
    name_zeit = StringProperty()
    founded_at = DateProperty(required=True)
    dissolved_at = DateProperty(required=False, )

    claims_territory = RelationshipTo(Territory, "TERRITORY", model=ClaimedTerritoryRel)

# class PointOfInterest(StructuredNode):
#     # geometry = PointProperty(crs='')
#     uid = UniqueIdProperty()


# class Population(StructuredNode):
#     date_census = DateProperty()
#     total = IntegerProperty()
#     by_language = JSONProperty()
#     by_faith = JSONProperty()
#     by_political_affiliation = JSONProperty()
#     by_gender = JSONProperty()
#     approximations = JSONProperty()  # maps field names to the degree of certainty in them
#
#
# class PersonOfInterest(StructuredNode):
#     uid = UniqueIdProperty()
#     name = StringProperty()
#     born_at = DateProperty()
#     deceased = DateProperty()


# class DataSource(StructuredNode):
#     uid = UniqueIdProperty()
#     description = StringProperty()
#     permalink = StringProperty()
