import os
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak)
from cpovc_registry.functions import search_person_name
from cpovc_forms.models import (
    OVCCaseRecord, OVCCaseGeo, OVCMedical, OVCCaseCategory, OVCFamilyStatus,
    OVCEconomicStatus)
from cpovc_registry.models import (
    RegPersonsExternalIds, RegPersonsGeo, RegPersonsSiblings,
    RegPersonsGuardians)
from cpovc_main.models import SetupGeography
from datetime import datetime

from django.conf import settings
from cpovc_main.functions import get_dict

STATIC_ROOT = settings.STATICFILES_DIRS[0]


current_directory = "%s" % (STATIC_ROOT)
checked_image_path = os.path.join(current_directory, 'images/checked.png')
unchecked_image_path = os.path.join(current_directory, 'images/unchecked.png')
logo_path = os.path.join(current_directory, 'images/gok_logo.png')

docs = {1: 'CASE Record Sheet'}


class FooterCanvas(canvas.Canvas):
    """Class to do footers."""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        # page = "Page %s of %s" % (self._pageNumber, page_count)
        page = "%s" % (self._pageNumber)
        footer = "Source of information relatives/teachers. "
        footer += "Indicate highest level of education attained. "
        footer += "Nearest landmark; School, Hospital, Church, Mosque."
        tfooter = 'This is a system generated document.'
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.25)
        self.line(22, 70, LETTER[0] - 42, 70)
        self.setFont('Times-Roman', 9)
        self.drawString(LETTER[0] - 70, 60, page)
        if self._pageNumber == 1:
            self.setFont('Times-Roman', 6)
            self.drawString(22, 60, footer)
        else:
            self.setFont('Times-Roman', 6)
            self.drawString(22, 60, tfooter)


def search_child(request, name):
    """Method to search child."""
    try:
        child_id = u"%s" % (name)
        if '/' in name:
            print('Search using serial number')
            cases = OVCCaseRecord.objects.filter(case_serial=name)
        elif child_id.isnumeric():
            print('Search of child ID')
            cid = int(name)
            cases = OVCCaseRecord.objects.filter(person_id=cid)
        else:
            cids = search_person_name(request, name)
            cases = OVCCaseRecord.objects.filter(person_id__in=cids)
    except Exception as e:
        print('Error getting CASES - %s' % (str(e)))
        return {}
    else:
        return cases


def get_check(item_value, item_check):
    """Method to get the checked value."""
    try:
        if item_value == item_check:
            img = checked_image_path
        else:
            img = unchecked_image_path
        if ',' in item_value:
            items = item_value.split(',')
            if item_check in items:
                img = checked_image_path
        chk_item = Image(img, .25 * cm, .25 * cm)
    except Exception as e:
        raise e
    else:
        return chk_item


def generate_crs(response, ovc_data, ovc_items):

    doc = SimpleDocTemplate(
        response, rightMargin=.5 * cm, leftMargin=.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
        title="Case Record Sheet", author='CPIMS',
        subject="CPIMS - Case Record Sheet", creator="CPIMS",
        keywords="CPIMS, DCS, Case Record Sheet")

    story = []
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    styles.add(ParagraphStyle(
        name='Line_Data', alignment=TA_LEFT, fontSize=8, leading=7))
    styles.add(ParagraphStyle(
        name='Line_Data_Small', alignment=TA_LEFT, fontSize=7, leading=8))
    styles.add(ParagraphStyle(
        name='Line_Data_Large', alignment=TA_LEFT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(
        name='Line_Data_Largest', alignment=TA_LEFT, fontSize=14, leading=15))
    styles.add(ParagraphStyle(
        name='Line_Label', font='Helvetica-Bold',
        fontSize=7, leading=7, alignment=TA_LEFT))
    styles.add(ParagraphStyle(
        name='Line_Title', font='Helvetica-Bold',
        fontSize=10, alignment=TA_LEFT))
    styles.add(ParagraphStyle(
        name='Line_Label_Center', font='Helvetica-Bold',
        fontSize=12, leading=10, alignment=TA_CENTER))

    # Get company information
    data1 = [[Image(logo_path, 1.8 * cm, 1.5 * cm)]]
    tt1 = Table(data1, colWidths=(None,), rowHeights=[0.5 * cm])
    sllc = styles["Line_Label_Center"]
    slds = styles["Line_Data_Small"]

    story.append(tt1)
    story.append(Paragraph("<b>DIRECTORATE OF CHILDREN SERVICES</b>", sllc))

    story.append(Spacer(0.1 * cm, .2 * cm))

    data1 = [[Paragraph('<b>CASE RECORD SHEET - A</b>', styles["Line_Title"]),
              Paragraph("<b><i>Rev. Aug '18</i></b>", slds)]]
    t1 = Table(data1, colWidths=(None, 2.0 * cm), rowHeights=[0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .1 * cm))
    intro = 'This form to be filled whenever a child protection issue is '
    intro += 'brought before a child protection office, institution '
    intro += ' or facility.'
    data1 = [[Paragraph(intro, styles["Line_Label"]), ]]
    t1 = Table(data1, colWidths=(None))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .1 * cm))
    data1 = [
        [Paragraph('<b>County:</b>', styles["Line_Label"]),
         Paragraph(ovc_data['county'], styles["Line_Data"]),
         Paragraph('<b>Sub County:</b>', styles["Line_Label"]),
         Paragraph(ovc_data['sub_county'], styles["Line_Data"]),
         Paragraph('<b>Institution:</b>', styles["Line_Label"]),
         Paragraph(ovc_data['institution'], styles["Line_Data"])]]

    t1 = Table(
      data1,
      colWidths=(1.4 * cm, 2.7 * cm, 2.0 * cm, 3.5 * cm, 2.0 * cm, None))
    t1.setStyle(TableStyle([
        ('INNERGRID', (1, 0), (1, 1), 0.25, colors.black),
        ('INNERGRID', (3, 0), (3, 1), 0.25, colors.black),
        ('INNERGRID', (5, 0), (5, 1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>Case Serial No:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['case_serial'], styles["Line_Data_Small"]),
              Paragraph('<b>Date of Reporting:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['case_date'], styles["Line_Data_Small"]),
              Paragraph('<b>Contact Address / Email:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['reporter_address'], slds)
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.4 * cm, 4.3 * cm, 2.1 * cm, 4.0 * cm, 2.5 * cm, 4.3 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Case Reported by (Name):</b>', styles["Line_Label"]),
              Paragraph(ovc_data['reporter_names'], styles["Line_Data_Small"]),
              Paragraph('<b>Relationship to Child:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['reporter_type'], styles["Line_Data_Small"]),
              Paragraph('<b>Telephone:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['reporter_tel'], styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.4 * cm, 4.3 * cm, 2.1 * cm, 4.0 * cm, 2.5 * cm, 4.3 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)

    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>PERSONAL DETAILS OF THE CHILD</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights = [0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>Name of Child:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['child_name'], styles["Line_Data_Small"]),
              Paragraph('<b>Date of Birth:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['ovc_dob'], styles["Line_Data_Small"]),
              Paragraph('<b>Sex:</b>', styles["Line_Label"]),
              Paragraph('Male', styles["Line_Label"]),
              get_check(ovc_data['sex'], 'SMAL'),
              Paragraph('Female', styles["Line_Data_Small"]),
              get_check(ovc_data['sex'], 'SFEM'),
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(
        2.4 * cm, 7.0 * cm, 1.5 * cm, 2.8 * cm, 1.9 * cm,
        1.4 * cm, 0.6 * cm, 1.4 * cm, 0.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (5, 0), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Child in School:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Name of School:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Class:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Category of School:</b>', styles["Line_Label"]),
              Paragraph('Formal', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Informal', styles["Line_Data_Small"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(
        2.4 * cm, 1.0 * cm, 2.0 * cm, 4.0 * cm, 1.5 * cm, 2.8 * cm,
        1.9 * cm, 1.4 * cm, 0.6 * cm, 1.4 * cm, 0.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (7, 0), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Tribe / Ethnicity:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['tribe'], styles["Line_Data_Small"]),
              Paragraph('<b>Name of closest friends of child: <sup>1</sup></b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Religion:</b>', styles["Line_Label"]),
              Paragraph('Protestant', styles["Line_Label"]),
              get_check(ovc_data['religion'], 'RECH'),
              Paragraph('Muslim', styles["Line_Label"]),
              get_check(ovc_data['religion'], 'REMU'),
              Paragraph('Catholic', styles["Line_Label"]),
              get_check(ovc_data['religion'], 'RECH'),
              Paragraph('Other', styles["Line_Data_Small"]),
              get_check(ovc_data['religion'], 'REOT'),
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(
        2.4 * cm, 3.0 * cm, 2.5 * cm, 2.1 * cm,
        1.6 * cm, 1.6 * cm, 0.5 * cm, 1.4 * cm,
        0.5 * cm, 1.4 * cm, 0.6 * cm, 1.4 * cm, 0.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (5, 0), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Mental Condition:</b>', styles["Line_Label"]),
              Paragraph('Normal', styles["Line_Data_Small"]),
              get_check(ovc_data['mental_cond'], 'MNRM'),
              Paragraph('Challenged', styles["Line_Label"]),
              get_check(ovc_data['mental_cond'], 'MCAV,MCAU'),
              Paragraph('<b>Physical Condition:</b>', styles["Line_Label"]),
              Paragraph('Normal', styles["Line_Data_Small"]),
              get_check(ovc_data['phy_cond'], 'PNRM'),
              Paragraph('Challenged', styles["Line_Label"]),
              get_check(ovc_data['phy_cond'], 'PHAV,PHAU'),
              Paragraph('<b>Other Medical Condition:</b>', styles["Line_Label"]),
              Paragraph('Normal', styles["Line_Label"]),
              get_check(ovc_data['other_cond'], 'CHNM'),
              Paragraph('Chronic', styles["Line_Data_Small"]),
              get_check(ovc_data['other_cond'], 'CHRO'),
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(
        2.4 * cm, 1.4 * cm, 0.6 * cm, 1.9 * cm, 0.6 * cm,
        2.0 * cm, 1.4 * cm, 0.6 * cm, 1.9 * cm, 0.6 * cm,
        2.2 * cm, 1.4 * cm, 0.6 * cm, 1.4 * cm, 0.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        ('INNERGRID', (4, 0), (6, 0), 0.25, colors.black),
        ('INNERGRID', (9, 0), (11, 0), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Hobbies:</b>', styles["Line_Label"]),
              Paragraph('Sports', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Movies', styles["Line_Data_Small"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Music', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Dancing', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Reading', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('<b>Child has Birth Certificate:</b>', styles["Line_Label"]),
              Paragraph('Yes', styles["Line_Label"]),
              get_check(ovc_data['bcert'], 'AYES'),
              Paragraph('No', styles["Line_Label"]),
              get_check(ovc_data['bcert'], 'ANNO'), 
              Paragraph('Refer to CRD.', styles["Line_Data_Small"]),
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(
        2.4 * cm, 1.4 * cm, 0.6 * cm, 1.4 * cm, 0.6 * cm, 1.2 * cm, 0.6 * cm,
        1.4 * cm, 0.6 * cm, 1.4 * cm, 0.6 * cm, 2.4 * cm,
        1.0 * cm, 0.6 * cm, 0.8 * cm, 0.6 * cm, 2.0 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        ('INNERGRID', (10, 0), (12, 0), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    # SIBLINGS
    data1 = [[Paragraph('<b>SIBLINGS</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights = [0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>No.</b>', styles["Line_Label"]),
              Paragraph('<b>Name</b>', styles["Line_Label"]),
              Paragraph('<b>D.O.B</b>', styles["Line_Label"]),
              Paragraph('<b>Sex</b>', styles["Line_Label"]),
              Paragraph('<b>Name of School</b>', styles["Line_Label"]),
              Paragraph('<b>Class</b>', styles["Line_Label"]),
              Paragraph('<b>Remarks</b>', styles["Line_Label"])],
    ]

    t1 = Table(data1, colWidths=(
        0.9 * cm, 5.0 * cm, 2.5 * cm, 1.5 * cm, 5 * cm,
        1.5 * cm, 3.2 * cm), rowHeights = [0.6 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    siblings = ovc_items['siblings']
    items = [{'sibling': i} for i in range (1, 9)]
    data1 = [[Paragraph(str(product['sibling']), styles["Line_Data"]),
             Paragraph(str(siblings[product['sibling']]['name']), styles["Line_Data"]),
             Paragraph(str(siblings[product['sibling']]['dob']), styles["Line_Data"]),
             Paragraph(str(siblings[product['sibling']]['sex']), styles["Line_Data"]),
             '','',
             Paragraph(str(siblings[product['sibling']]['remark']), styles["Line_Data"])] for product in items]

    t1 = Table(data1, colWidths=(
        0.9 * cm, 5.0 * cm, 2.5 * cm, 1.5 * cm, 5 * cm, 1.5 * cm, 3.2 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1) 
    story.append(Spacer(0.1 * cm, .2 * cm))
    # HOME PARTICULARS
    data1 = [[Paragraph('<b>HOME PARTICULARS OF THE CHILD</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights = [0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>County:<br/></b>', styles["Line_Label"]),
              Paragraph(ovc_data['child_county'], styles["Line_Data_Small"]),
              Paragraph('<b>Sub-County:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['child_sub_county'], styles["Line_Data_Small"]),
              Paragraph('<b>Village/Estate:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"])
             ]]

    t1 = Table(data1, colWidths=(
        2.4 * cm, 4.3 * cm, 2.1 * cm, 4.0 * cm, 2.5 * cm,
        4.3 * cm), rowHeights = [0.6 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Ward:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['child_ward'], styles["Line_Data_Small"]),
              Paragraph('<b>Nearest Land Mark:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"])
              ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.4 * cm, 4.3 * cm, 2.1 * cm, 10.8 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    hes_txt = '<b>Household Economic Status (Income):</b>'
    data1 = [[Paragraph('<b>Family Status:</b>', styles["Line_Label"]),
              Paragraph('Parents living together', styles["Line_Label"]),
              get_check(ovc_data['family_status'], ''),
              Paragraph('Parents not living together', styles["Line_Label"]),
              get_check(ovc_data['family_status'], 'FSPN'),
              Paragraph(hes_txt, styles["Line_Label"]),
              Paragraph('Low', styles["Line_Label"]),
              get_check(ovc_data['hes_status'], 'LINC'),
              Paragraph('Middle', styles["Line_Label"]),
              get_check(ovc_data['hes_status'], 'MINC'),
              Paragraph('High', styles["Line_Label"]),
              get_check(ovc_data['hes_status'], 'HINC'),
              Paragraph('Unknown', styles["Line_Label"]),
              get_check(ovc_data['hes_status'], 'UINC')
              ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(
        2.4 * cm, 2.6 * cm, 0.6 * cm, 2.6 * cm, 0.6 * cm,
        3.1 * cm, 1.1 * cm, 0.6 * cm, 1.4 * cm, 0.7 * cm,
        1.1 * cm, 0.7 * cm, 1.5 * cm, 0.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        ('INNERGRID', (4, 0), (6, 0), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    # PARENTS PARTICULARS
    data1 = [[Paragraph('<b>PARENTS PARTICULARS</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights=[0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>Name</b>', styles["Line_Label"]),
              Paragraph('<b>Relationship</b>', styles["Line_Label"]),
              Paragraph('<b>ID No.</b>', styles["Line_Label"]),
              Paragraph('<b>Date of Birth</b>', styles["Line_Label"]),
              Paragraph('<b>Telephone</b>', styles["Line_Label"]),
              Paragraph('<b>Village/Estate</b>', styles["Line_Label"]),
              Paragraph('<b>Occupation</b>', styles["Line_Label"]),
              Paragraph('<b>Education<sup>2</sup></b>', styles["Line_Label"]),
              Paragraph('<b>Alive</b>', styles["Line_Label"])
              ]]

    t1 = Table(data1, colWidths=(
        4.5 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 2.1 * cm, 2.0 * cm,
        1.8 * cm, 1.1 * cm), rowHeights=[0.6 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    sld = styles["Line_Data"]
    story.append(t1)
    parents_items = {1: 'Father', 2: 'Mother'}
    parents = ovc_data['parents']
    items = [{'parent': 1}, {'parent': 2}]
    data1 = [[Paragraph(str(parents[product['parent']]['name']), sld),
              Paragraph(str(parents_items[product['parent']]), sld),
              '',
              Paragraph(str(parents[product['parent']]['dob']), sld),
              '','', '', '', ''] for product in items]

    t1 = Table(data1, colWidths=(4.5 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 2.1 * cm, 2.0 * cm, 1.8 * cm, 1.1 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1) 
    story.append(Spacer(0.1 * cm, .2 * cm))
    # CAREGIVERS
    data1 = [[Paragraph('<b>CAREGIVER PARTICULARS</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights = [0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .1 * cm))
    data1 = [[Paragraph('<b>Relationship:</b>', styles["Line_Label"]),
              Paragraph('Foster Parent', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Guardian', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Next of Kin', styles["Line_Label"]),
              Image(unchecked_image_path, .25 * cm, .25 * cm),
              Paragraph('Select as appropriate for caregiver', styles["Line_Label"]),]
    ]
    t1 = Table(data1, colWidths=(2.5 * cm, 2.0 * cm, 0.6 * cm, 1.5 * cm, 0.6 * cm, 2.0 * cm, 0.6 * cm, None))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .1 * cm))
    data1 = [[Paragraph('<b>Name</b>', styles["Line_Label"]),
              Paragraph('<b>Sex</b>', styles["Line_Label"]),
              Paragraph('<b>Relationship</b>', styles["Line_Label"]),
              Paragraph('<b>ID No.</b>', styles["Line_Label"]),
              Paragraph('<b>Date of Birth</b>', styles["Line_Label"]),
              Paragraph('<b>Telephone</b>', styles["Line_Label"]),
              Paragraph('<b>Village/Estate</b>', styles["Line_Label"]),
              Paragraph('<b>Occupation</b>', styles["Line_Label"]),
              Paragraph('<b>Education<sup>2</sup></b>', styles["Line_Label"])],
    ]

    t1 = Table(data1, colWidths=(
        4.5 * cm, 1.1 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm,
        2.1 * cm, 2.0 * cm, 1.8 * cm), rowHeights=[0.6 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    items = [{'caregiver': 1}, {'caregiver': 2}]
    caregivers = ovc_data['caregivers']
    data1 = [[Paragraph(str(caregivers[product['caregiver']]['name']), sld),
              '', '', '', '', '', '', '', ''] for product in items]

    t1 = Table(data1, colWidths=(
        4.5 * cm, 1.1 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm,
        2.0 * cm, 2.1 * cm, 2.0 * cm, 1.8 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    # story.append(Spacer(0.5 * cm, 2.5 * cm))
    story.append(PageBreak())
    # CASE HISTORY
    data1 = [[Paragraph('<b>CASE HISTORY OF THE CHILD</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights = [0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>Date of Event / incident:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['case_date'], styles["Line_Data_Small"]),
              Paragraph('<b>Place of Event / incident:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['case_place'], styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 7.0 * cm, 2.6 * cm, 7.0 * cm), rowHeights = [1.2 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Alleged Perpetrator / Offender:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['perpetrator'], styles["Line_Data_Small"]),
              Paragraph('<b>Relationship to the Child:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['perpetrator_relation'], styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 7.0 * cm, 2.6 * cm, 7.0 * cm), rowHeights = [1.2 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Case category:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['case_category'], styles["Line_Data_Small"]),
              Paragraph('<b>Specific issue about the case:</b>', styles["Line_Label"]),
              Paragraph(ovc_data['case_remarks'], styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 7.0 * cm, 2.6 * cm, 7.0 * cm), rowHeights = [1.2 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Nature of case:</b>', styles["Line_Label"]),
              Paragraph('One off event', styles["Line_Label"]),
              get_check(ovc_data['case_nature'], 'OOEV'),
              Paragraph('Chronic / On going event', styles["Line_Label"]),
              get_check(ovc_data['case_nature'], 'OCGE'),
              Paragraph('Emergency', styles["Line_Label"]),
              get_check(ovc_data['case_nature'], 'OCME'),
              Paragraph('<b>Risk Level:</b>', styles["Line_Label"]),
              Paragraph('Low', styles["Line_Label"]),
              get_check(ovc_data['risk_level'], 'RLLW'),
              Paragraph('Medium', styles["Line_Label"]),
              get_check(ovc_data['risk_level'], 'RLMD'),
              Paragraph('High', styles["Line_Label"]),
              get_check(ovc_data['risk_level'], 'RLHG')
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(
        2.9 * cm, 1.5 * cm,  0.6 * cm, 1.9 * cm,  0.6 * cm,  1.8 * cm,  0.6 * cm,
        2.6 * cm, 1.5 * cm,  0.6 * cm, 1.9 * cm,  0.6 * cm,  1.8 * cm,  0.6 * cm), rowHeights = [0.6 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        ('INNERGRID', (6, 0), (8, 0), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Needs of the Child:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('', styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 8.3 * cm, 8.3 * cm), rowHeights = [0.6 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Action Taken (Intervention):</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 16.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    refto = [[Paragraph('<b>State Agency (Specify):</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Reason for referral:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"])
             ],
             [Paragraph('<b>Non-State Agency (Specify):</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Reason for referral:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"])
             ]]
    rt0 = Table(refto, colWidths=(4.0 * cm, None, 3.0 * cm, None))
    rt0.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (0, 1), 0.25, colors.black),
        ('INNERGRID', (1, 0), (1, 1), 0.25, colors.black),
        ('INNERGRID', (2, 0), (2, 1), 0.25, colors.black),
        ('INNERGRID', (3, 0), (3, 1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    data1 = [[Paragraph('<b>Refferal to:</b>', styles["Line_Label"]),
              rt0
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 16.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    # RECOMMENDATIONS
    data1 = [[Paragraph('<b>RECOMMENDATIONS FOR FURTHER ASSISTANCE BASED ON THE BEST INTEREST OF THE CHILD (BIC)</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights = [0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [['']]
    t1 = Table(data1, colWidths=(19.6 * cm), rowHeights = [1.8 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        ('INNERGRID', (0, 1), (1, 1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>Name of Officer:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Signature:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 7.0 * cm, 2.7 * cm, 7.0 * cm), rowHeights = [0.8 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    data1 = [[Paragraph('<b>Designation:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"]),
              Paragraph('<b>Date:</b>', styles["Line_Label"]),
              Paragraph('', styles["Line_Data_Small"])
             ]]

    # t1 = Table(data1, colWidths=(3 * cm, None, 4.5 * cm,))
    t1 = Table(data1, colWidths=(2.9 * cm, 7.0 * cm, 2.7 * cm, 7.0 * cm), rowHeights = [0.8 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    # FOLLOW UP
    data1 = [[Paragraph('<b>FOLLOW UP INFORMATION (INDICATE ANY PROGRESS FOR FURTHER INVERVENTION GIVEN)</b>', styles["Line_Title"])]]
    t1 = Table(data1, colWidths=(None,), rowHeights = [0.5 * cm])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), '#a7a5a5'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    story.append(Spacer(0.1 * cm, .2 * cm))
    data1 = [[Paragraph('<b>Date</b>', styles["Line_Label"]),
              Paragraph('<b>Follow Up Status</b>', styles["Line_Label"]),
              Paragraph('<b>Comment</b>', styles["Line_Label"]),
              Paragraph('<b>Officer</b>', styles["Line_Label"])],
    ]

    t1 = Table(data1, colWidths=(3.0 * cm, 4.5 * cm, 6.0 * cm, 6.1 * cm), rowHeights = [0.6 * cm])
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1)
    t0 = Table([[Paragraph('Name', styles["Line_Label"])],
                [Paragraph('Designation', styles["Line_Label"])],
                [Paragraph('Signature', styles["Line_Label"])]], colWidths=(None))
    t0.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    items = [{'followup': i} for i in range (1, 4)]
    data1 = [['','','',t0] for product in items]

    t1 = Table(data1, colWidths=(3.0 * cm, 4.5 * cm, 6.0 * cm, 6.1 * cm))

    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t1) 
    # FOOTER
    story.append(Spacer(0.1 * cm, .2 * cm))
    story.append(Table([[Paragraph('I DECLARE THE INFORMATION CONTAINED IN THIS '
                                   'DOCUMENT TO BE TRUE AND CORRECT AS RECORDED IN CPIMS', styles["Line_Label"])]]))

    story.append(Spacer(0.1 * cm, .2 * cm))

    # TODO: signature could be image ? Date could be sign_date ?
    # TODO: signature, date
    data1 = [
        ['', '',
         Paragraph(ovc_data['document_date'], styles["Line_Data_Large"])
        ],
        [Paragraph('SIGNATURE OF SCCO (Must be signed for official use.)', styles["Line_Label"]), '',
         Paragraph('DATE', styles["Line_Label"])]]

    t1 = Table(data1, colWidths=(None, 2*cm, None))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (0, 1), 0.25, colors.black),
        ('INNERGRID', (2, 0), (2, 1), 0.25, colors.black),
    ]))

    story.append(t1)

    doc.build(story, canvasmaker=FooterCanvas)


def validate_case(request, case_id):
    """Method to validate case ownership."""
    try:
        is_valid = True
        case = OVCCaseGeo.objects.get(case_id_id=case_id)
    except Exception as e:
        print('Error validating case - %s' % (str(e)))
        return None, None
    else:
        return case, is_valid


def param_val(val, values):
    """Get param values."""
    return values[val] if val in values else val


def get_area(area_id):
    """Method to get the area details."""
    try:
        area = SetupGeography.objects.get(area_id=area_id)
        return area.area_name
    except Exception as e:
        print('Error %s' % (str(e)))
        return 'N/A'


def generate_form(request, response, doc_id, case):
    """Method to generate form."""
    try:
        # Settings
        child_id = case.person_id
        case_id = case.case_id_id
        check_fields = ['case_reporter_id', 'identifier_type_id',
                        'religion_type_id', 'tribe_category_id',
                        'event_place_id', 'perpetrator_status_id',
                        'relationship_type_id', 'case_category_id']
        vals = get_dict(field_name=check_fields)
        case_serial = case.case_id.case_serial
        sub_county = case.report_subcounty.area_name
        county_id = case.report_subcounty.parent_area_id
        case_open_date = case.case_id.date_case_opened
        case_date = str(case_open_date.strftime('%d %b, %Y'))
        # County
        county = get_area(county_id)
        # Org Unit
        org_unit = case.report_orgunit.org_unit_name
        # Reporter
        reporter_address = case.case_id.case_reporter_contacts
        reporter_fname = case.case_id.case_reporter_first_name
        reporter_sname = case.case_id.case_reporter_surname
        reporter_oname = case.case_id.case_reporter_other_names
        roname = reporter_oname if reporter_oname else ''
        rsname = reporter_sname if reporter_sname else ''
        rfname = reporter_fname if reporter_fname else ''
        reporter_names = '%s %s %s' % (rfname, rsname, roname)
        # Perpetrator
        perp_status = case.case_id.perpetrator_status
        perp_relation = param_val(
            case.case_id.perpetrator_relationship_type, vals)
        perpetrator_relation = perp_relation if perp_relation else ''
        print('PERP', perp_status)
        if perp_status == 'PKNW':
            perp_fname = case.case_id.perpetrator_first_name
            perp_sname = case.case_id.perpetrator_surname
            perp_oname = case.case_id.perpetrator_other_names
            poname = perp_oname if perp_oname else ''
            psname = perp_sname if perp_sname else ''
            pfname = perp_fname if perp_fname else ''
            perpetrator = '%s %s %s' % (pfname, psname, poname)
        else:
            perpetrator = param_val(perp_status, vals)
        reporter_type = param_val(case.case_id.case_reporter, vals)
        reporter_tel = reporter_address if reporter_address else 'N/A'
        risk_level = case.case_id.risk_level
        case_remarks = case.case_id.case_remarks
        case_info = case_remarks if case_remarks else ''
        # Child details
        ovc_fname = case.case_id.person.first_name
        ovc_onames = case.case_id.person.other_names
        ovc_sname = case.case_id.person.surname
        ovc_oname = ovc_onames if ovc_onames else ''
        child_name = '%s %s %s (%s)' % (ovc_fname, ovc_sname,
                                        ovc_oname, str(child_id))
        ovc_sex = case.case_id.person.sex_id
        dob = case.case_id.person.date_of_birth
        ovc_dob = str(dob.strftime('%d %b, %Y')) if dob else 'N/A'
        # Geo
        child_sub_county, child_ward, child_county_id = 'N/A', 'N/A', 0
        child_geos = RegPersonsGeo.objects.filter(
            person_id=child_id, is_void=False)
        for child_geo in child_geos:
            area_id = child_geo.area_id
            if area_id > 337:
                child_ward = child_geo.area.area_name
            else:
                child_sub_county = child_geo.area.area_name
                child_county_id = child_geo.area.parent_area_id
            area_type = child_geo.area_type
            print('A TYPE', area_type)
        child_county = get_area(child_county_id)
        # Siblings
        siblings, sid = {}, 0
        child_siblings = RegPersonsSiblings.objects.filter(
            child_person_id=child_id)
        for cs in child_siblings:
            sid += 1
            sib_id = str(cs.sibling_person_id)
            dob = cs.sibling_person.date_of_birth
            ssex = 'Male' if cs.sibling_person.sex_id == 'SMAL' else 'Female'
            sdob = str(dob.strftime('%d %b, %Y')) if dob else 'N/A'
            child_sib = {'name': str(cs.sibling_person.first_name),
                         'dob': sdob, 'sex': ssex, 'remark': sib_id}
            siblings[sid] = child_sib
        if sid < 8:
            for i in range(sid + 1, 9):
                siblings[i] = {'name': '', 'dob': '', 'sex': '', 'remark': ''}
        # Caregivers / Parents
        cgnt = 0
        pts = {'name': 'N/A', 'dob': '', 'idno': ''}
        ptf = {'name': 'N/A', 'dob': '', 'idno': ''}
        cgs = {'name': 'N/A', 'dob': '', 'idno': ''}
        cgf = {'name': 'N/A', 'dob': '', 'idno': ''}
        parents, guardians = {1: pts, 2: ptf}, {1: cgs, 2: cgf}
        caregivers = RegPersonsGuardians.objects.filter(
            child_person_id=child_id)
        for caregiver in caregivers:
            relation = caregiver.relationship
            cg_fname = caregiver.guardian_person.first_name
            cg_sname = caregiver.guardian_person.surname
            cg_name = '%s %s' % (str(cg_fname), str(cg_sname))
            cg_dob = caregiver.guardian_person.date_of_birth
            if relation == 'CGPM':
                parents[2]['name'] = cg_name
                parents[2]['dob'] = cg_dob
            elif relation == 'CGPF':
                parents[1]['name'] = cg_name
                parents[1]['dob'] = cg_dob
            else:
                cgnt += 1
                guardians[cgnt]['name'] = cg_name
                guardians[cgnt]['relation'] = relation
                guardians[cgnt]['dob'] = cg_dob

        # Child external ids
        extids = RegPersonsExternalIds.objects.filter(
            person_id=child_id, is_void=False)
        tribe, religion, bcert = '', '', 'ANNO'
        for extid in extids:
            if extid.identifier_type_id == 'ITRB':
                tribe = param_val(extid.identifier, vals)
            if extid.identifier_type_id == 'IREL':
                religion = extid.identifier
            if extid.identifier_type_id == 'RGBC':
                bcert = 'AYES'
        # Get medical
        meds = OVCMedical.objects.get(case_id_id=case_id)
        phy_cond = meds.physical_condition
        mental_cond = meds.mental_condition
        other_cond = meds.other_condition
        # Case details
        case_datas = OVCCaseCategory.objects.filter(case_id_id=case_id)
        for case_data in case_datas:
            case_date = str(case_data.date_of_event.strftime('%d %b, %Y'))
            case_place = param_val(case_data.place_of_event, vals)
            case_category = param_val(case_data.case_category, vals)
            case_nature = case_data.case_nature
        # Family status
        family_status = ''
        family_statuses = OVCFamilyStatus.objects.filter(
            case_id_id=case_id, is_void=False)
        for fstatus in family_statuses:
            family_status = str(fstatus.family_status)
        # HES
        hes_status = ''
        hess = OVCEconomicStatus.objects.filter(
            case_id_id=case_id, is_void=False)
        for hes in hess:
            hes_status = str(hes.household_economic_status)
            print(hes_status)
        # Dates
        todate = datetime.now()
        reporter_name = reporter_names.replace('  ', ' ').capitalize()
        doc_date = str(todate.strftime('%d %b, %Y'))
        ovc_data = {'org_unit': org_unit,
                    'child_name': child_name.replace('  ', ' '),
                    'tribe': tribe, 'religion': religion,
                    'case_date': case_date, 'reporter_address': 'N/A',
                    'reporter_tel': reporter_tel,
                    'reporter_type': reporter_type,
                    'reporter_names': reporter_name,
                    'ovc_dob': ovc_dob, 'document_date': doc_date,
                    'parents': parents, 'caregivers': guardians,
                    'registration_date': 'Jan 20, 2017', 'county': county,
                    'sub_county': sub_county, 'sex': ovc_sex,
                    'institution': org_unit, 'case_serial': case_serial,
                    'phy_cond': phy_cond, 'mental_cond': mental_cond,
                    'other_cond': other_cond,
                    'bcert': bcert, 'case_date': case_date,
                    'case_place': case_place, 'hes_status': hes_status,
                    'perpetrator': perpetrator.capitalize(),
                    'perpetrator_relation': perpetrator_relation,
                    'case_category': case_category,
                    'case_nature': case_nature, 'family_status': family_status,
                    'risk_level': risk_level, 'child_county': child_county,
                    'case_remarks': case_info, 'child_ward': child_ward,
                    'child_sub_county': child_sub_county}

        services = {'service_date': 'Jan 10, 2017', 'service_type': 'SERVICE',
                    'service_name': 'description'}

        ovc_items = {'services': services, 'siblings': siblings}
        print(ovc_data)
        print(ovc_items)
        generate_crs(response, ovc_data, ovc_items)
    except Exception as e:
        print('error generating document - %s' % (str(e)))
        raise e
    else:
        pass
