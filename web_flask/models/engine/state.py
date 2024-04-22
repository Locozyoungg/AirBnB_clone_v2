if os.getenv('HBNB_TYPE_STORAGE') != 'db':
    @property
    def cities(self):
        """Returns the list of City objects linked to the current State"""
        from models import storage
        cities = []
        for city in storage.all(City).values():
            if city.state_id == self.id:
                cities.append(city)
        return cities

