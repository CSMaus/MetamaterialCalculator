# we'll define materials as data structure for vars creations
# their properties would be binded and dynamically updated with GUI updates

class PorousMaterial:
    def __init__(self, update_callback: callable = None):
        super().__init__()
        # TODO: check all this parameters correctness
        self._properties = {
            "viscous_cl": None,  # Viscous Characteristic Length [m]
            "thermal_cl": None,  # Thermal Characteristic Length [m]
            "density": None,  # Density [kg/m³]
            "airflow_resistivity": None,  # Airflow Resistivity [Pa·s/m²]
            "tortuosity": None,  # Tortuosity
            "porosity": None,  # Porosity
            "loss_factor": None,  # Loss Factor
            "poissons_ratio": None  # Poisson’s Ratio
        }

        self.update_callback = update_callback

    def get_property(self, key):
        return self._properties.get(key, None)

    def set_property(self, key, value):
        if key in self._properties:
            self._properties[key] = value
            if self.update_callback:
                self.update_callback(key, value)
        else:
            raise KeyError(f"Property '{key}' does not exist in PorousMaterial")

class SolidMaterial:
    def __init__(self, update_callback: callable = None):
        super().__init__()

        self._properties = {
            "static_youngs_modulus": None, # Static Young's Modulus [Pa]
            "density": None,
            "loss_factor": None,
            "poissons_ratio": None
        }

        self.update_callback = update_callback

    def get_property(self, key):
        return self._properties.get(key, None)

    def set_property(self, key, value):
        if key in self._properties:
            self._properties[key] = value
            if self.update_callback:
                self.update_callback(key, value)
        else:
            raise KeyError(f"Property '{key}' does not exist in PorousMaterial")

class PorousMaterial_old:
    def __init__(self, update_callback: callable = None):
        super().__init__()

        self.viscous_cl = None  # Viscous Characteristic Length [m]
        self.thermal_cl = None  # Thermal Characteristic Length [m]
        self.density = None  # Density [kg/m³]
        self.airflow_resistivity = None  # Airflow Resistivity [Pa·s/m²]
        self.tortuosity = None  # Tortuosity
        self.porosity = None  # Porosity
        self.loss_factor = None  # Loss Factor
        self.poissons_ratio = None  # Poisson’s Ratio

        self.update_callback = update_callback

    # property decorators to implement gui triggers so later
    # when reading material values from table
    # gui would automatically update
    @property
    def viscous_cl(self):
        return self._viscous_cl
    @property
    def thermal_cl(self):
        return self.thermal_cl
    @property
    def density(self):
        return self.density
    @property
    def airflow_resistivity(self):
        return self.airflow_resistivity
    @property
    def tortuosity(self):
        return self.tortuosity
    @property
    def porosity(self):
        return self.porosity
    @property
    def loss_factor(self):
        return self.loss_factor
    @property
    def poissons_ratio(self):
        return self.poissons_ratio

    @viscous_cl.setter
    def viscous_cl(self, value):
        self._viscous_cl = value
        if self.update_callback:
            self.update_callback("viscous_cl", value)
    @airflow_resistivity.setter
    def airflow_resistivity(self, value):
        self._airflow_resistivity = value
        if self.update_callback:
            self.update_callback("airflow_resistivity", value)
    @thermal_cl.setter
    def thermal_cl(self, value):
        self._thermal_cl = value
        if self.update_callback:
            self.update_callback("thermal_cl", value)
    @density.setter
    def density(self, value):
        self._density = value
        if self.update_callback:
            self.update_callback("density", value)
    @tortuosity.setter
    def tortuosity(self, value):
        self._tortuosity = value
        if self.update_callback:
            self.update_callback("tortuosity", value)
    @porosity.setter
    def porosity(self, value):
        self._porosity = value
        if self.update_callback:
            self.update_callback("porosity", value)
    @loss_factor.setter
    def loss_factor(self, value):
        self._loss_factor = value
        if self.update_callback:
            self.update_callback("loss_factor", value)
    @poissons_ratio.setter
    def poissons_ratio(self, value):
        self._poissons_ratio = value
        if self.update_callback:
            self.update_callback("poissons_ratio", value)




