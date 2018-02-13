# Convertisseurs
class ReelConverter:
    # Attributs
    regex = "[0-9]+\.?[0-9]*"

    # Méthodes
    def to_python(self, val):
        return float(val)

    def to_url(self, val):
        return "{:f}".format(val)