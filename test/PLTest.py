from Property import Property
from PropertyListings import PropertyListings

properties = PropertyListings('../data/testWriteProperties.json')

property1 = Property('Toronto', 'house', 500, ['TV', 'Hot hub', 'Pet friendly'], ['remote', 'nightlife'])
property2 = Property('Vancouver', 'cabin', 430, ['parking', 'gym'], ['urban', 'lakefront'])
property3 = Property('Montreal', 'condo', 650, ['garden', 'patio'], ['quiet'])

properties.add_property(property1)
properties.add_property(property2)
properties.add_property(property3)

properties.view_properties()