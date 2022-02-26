import datetime
from django import forms
from .functions import get_ip

county_vars = (('0', 'National'),
               ('030', 'Baringo'),
               ('036', 'Bomet'),
               ('039', 'Bungoma'),
               ('040', 'Busia'),
               ('028', 'Elgeyo Marakwet'),
               ('014', 'Embu'),
               ('007', 'Garissa'),
               ('043', 'Homa Bay'),
               ('011', 'Isiolo'),
               ('034', 'Kajiado'),
               ('037', 'Kakamega'),
               ('035', 'Kericho'),
               ('022', 'Kiambu'),
               ('003', 'Kilifi'),
               ('020', 'Kirinyaga'),
               ('045', 'Kisii'),
               ('042', 'Kisumu'),
               ('015', 'Kitui'),
               ('002', 'Kwale'),
               ('031', 'Laikipia'),
               ('005', 'Lamu'),
               ('016', 'Machakos'),
               ('017', 'Makueni'),
               ('009', 'Mandera'),
               ('010', 'Marsabit'),
               ('012', 'Meru'),
               ('044', 'Migori'),
               ('001', 'Mombasa'),
               ('021', "Murang'a"),
               ('047', 'Nairobi'),
               ('032', 'Nakuru'),
               ('029', 'Nandi'),
               ('033', 'Narok'),
               ('046', 'Nyamira'),
               ('018', 'Nyandarua'),
               ('019', 'Nyeri'),
               ('025', 'Samburu'),
               ('041', 'Siaya'),
               ('006', 'Taita Taveta'),
               ('004', 'Tana River'),
               ('013', 'Thara Nithi'),
               ('026', 'Trans Nzoia'),
               ('023', 'Turkana'),
               ('027', 'Uasin Gishu'),
               ('038', 'Vihiga'),
               ('008', 'Wajir'),
               ('024', 'West Pokot'))

const_vars = (('0', 'All Constituencies'),)

ward_vars = (('', 'All Wards'),)

ip_vars = get_ip()

lip_vars = (('', 'All LIPs'),)

period_vars = (('1', 'APR'), ('2', 'SAPR'), )

fy_vars = (('21', 'FY21'), ('22', 'FY22'), )

fund_vars = (('', 'All Funding Mechanisms'), ('1', 'USAID'),
             ('2', 'CDC'), ('3', 'DoD'),)


class CaseLoad(forms.Form):
    """Class for case load reports forms."""

    def __init__(self, *args, **kwargs):
        """Constructor for override especially on fly data."""
        super(CaseLoad, self).__init__(*args, **kwargs)

        today = datetime.date.today()
        year = today.strftime('%Y')
        mwezi = today.strftime('%m')
        mwaka = (int(year) + 1) if int(mwezi) > 9 else int(year)
        years = [(yr, '%s/%s' % (yr, yr + 1)) for yr in range(2020, mwaka)]
        year_tuple = tuple(years)

        sel_year = forms.ChoiceField(
            choices=year_tuple,
            initial=year,
            widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-year', 'data-size': '3',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))
        self.fields['sel_year'] = sel_year

    sel_county = forms.ChoiceField(
        choices=county_vars,
        initial='',
        widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-county', 'data-size': '10',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))

    sel_constituency = forms.ChoiceField(
        choices=const_vars,
        initial='0',
        widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-constituency', 'data-size': '5',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))

    sel_ward = forms.ChoiceField(
        choices=ward_vars,
        initial='0',
        widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-ward', 'data-size': '5',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))

    sel_ip = forms.ChoiceField(
        choices=ip_vars,
        initial='0',
        widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-ip', 'data-size': '5',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))

    sel_lip = forms.ChoiceField(
        choices=lip_vars,
        initial='0',
        widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-lip', 'data-size': '5',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))

    sel_period = forms.ChoiceField(
        choices=period_vars,
        initial='0',
        widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-period', 'data-size': '5',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))

    sel_funding = forms.ChoiceField(
        choices=fund_vars,
        initial='0',
        widget=forms.Select(
                attrs={'class': 'form-control selectpicker',
                       'id': 'sel-funding', 'data-size': '5',
                       'data-live-search': 'true',
                       'data-style': 'btn-white',
                       'autofocus': 'true'}))
