import yt

class FieldAdder:

    @staticmethod
    def AddFields():
        yt.add_field(
            ('gas', 'electron_density'), 
            function=FieldAdder.electron_density, 
            sampling_type='cell',
            units='cm**(-3)',
            force_override=True
        )

        yt.add_field(
            ('gas', 'eint'), 
            function=FieldAdder.eint, 
            sampling_type='cell',
            units='erg/g',
            force_override=True
        )

        yt.add_field(
            ('gas', 'temp_in_keV'), 
            function=FieldAdder.correctedTempInKeV, 
            sampling_type='cell',
            units='keV',
            force_override=True
        )

        yt.add_field(
            ('gas', 'correctedTemp'), 
            function=FieldAdder.correctedTemp, 
            sampling_type='cell',
            units='K',
            force_override=True
        )

        yt.add_field(
            ("gas", "entropy"), 
            function = FieldAdder.entropy, 
            sampling_type='cell', 
            units='keV*cm**2',
            force_override=True
        )

        yt.add_field(
            ("gas", "potential"), 
            function = FieldAdder.potential, 
            sampling_type='cell', 
            units='erg/g',
            force_override=True
        )

        yt.add_field(
            ('gas', 'density'), 
            function=FieldAdder.density, 
            sampling_type='cell',
            units='g*cm**(-3)',
            force_override=True
        )

        yt.add_field(
            ('gas', 'pressure'), 
            function=FieldAdder.pressure, 
            sampling_type='cell',
            units='Ba',
            force_override=True
        )


        yt.add_field(
            ('gas', 'radius'), 
            function=FieldAdder.radius, 
            sampling_type='cell',
            units='kpc',
            force_override=True
            )
        

    @staticmethod
    def electron_density(field, data):
        return data[('flash', 'dens')]/(yt.units.atomic_mass_unit_cgs*1.18)

    @staticmethod
    def eint(field, data):
        return (3/2)*(data[('gas', 'pressure')]/data[('gas', 'density')])

    @staticmethod
    def correctedTempInKeV(field, data):
        return (2./3.)*(0.62*yt.units.atomic_mass_unit_cgs*data[('gas', 'eint')])
    
    @staticmethod
    def correctedTemp(field, data):
        return data[('gas', 'temp_in_keV')]/yt.units.boltzmann_constant_cgs

    @staticmethod
    def entropy(field, data):
        return data[("gas", "temp_in_keV")] * data[('gas', 'electron_density')]**(-2/3)

    @staticmethod
    def potential(field, data):
        return data[('flash', 'gpot')] * (-1)

    @staticmethod
    def density(field, data):
        return data[('flash', 'dens')]

    @staticmethod
    def pressure(field, data):
        return data[('flash', 'pres')]
    
    @staticmethod
    def radius(field, data):
        return data['index', 'radius']
    