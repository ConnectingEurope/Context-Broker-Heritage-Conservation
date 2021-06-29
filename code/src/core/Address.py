# address class. Country code and city
class Address:
    def __init__(self,country,city):
        self.addressCountry         = country
        self.addressLocality        = city
        self.type                   = "PostalAddress"
