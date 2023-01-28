import pandas as pd
# import numpy as np
from django.db import connection, connections
from datetime import datetime
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, landscape, portrait
# Security
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from reportlab.platypus import Flowable
from django.conf import settings
from .dq_queries import TXT


class Blank(object):
    index = []
    columns = []

    def __init__(self):
        self.index = []
        self.columns = []
        self.vars = {}


class Canvas(canvas.Canvas):
    """Pagination extention for canvas."""

    def __init__(self, *args, **kwargs):
        """Constructor for my pagination."""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.page = ''

    def showPage(self):
        """Get the pages first."""
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """To add page info to each page (page x of y)."""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        """Draw the final page."""
        self.page = "Page %d of %d" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 8)
        self.drawString(0.5 * inch, 0.38 * inch, self.page)


class BarCode(Flowable):
    """Barcode class."""

    def __init__(self, value="1234567890", ratio=2.1):
        """Init and store rendering value."""
        Flowable.__init__(self)
        self.value = value
        self.ratio = ratio

    def wrap(self, availwidth, availheight):
        """Make the barcode fill the width while maintaining the ratio."""
        self.width = availwidth
        self.height = self.ratio * availheight
        return self.width, self.height

    def draw(self):
        """Flowable canvas."""
        a4width, a4height = A4
        qr_code = qr.QrCodeWidget(self.value)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(65, 65, transform=[65. / width, 0, 0, 65. / height, 0, 0])
        d.add(qr_code)
        renderPDF.draw(d, self.canv, 45, height - 80)


def draw_page(canvas, doc):
    """Method to format my pdfs."""
    title = "CPIMS"
    author = "CPIMS"
    canvas.setTitle(title)
    canvas.setSubject(title)
    canvas.setAuthor(author)
    canvas.setCreator(author)
    # footer = []
    # Put some data into the footer
    # Frame(2 * cm, 0, 17 * cm, 4 * cm).addFromList(footer, canvas)
    canvas.saveState()

    # Header
    canvas.drawString(0.5 * inch, 8 * inch, doc.fund_name)
    canvas.drawRightString(10.5 * inch, 8 * inch, doc.report_info)

    # Footers
    pw, pl = doc.pagesize
    fl = 7.9 if pw < 600 else 11.2
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.5 * inch, 0.5 * inch, '')
    canvas.drawRightString(
        fl * inch, 0.38 * inch, 'Source : %s' % (doc.source))

    canvas.setFont("Helvetica", 240)
    # self.setFont("Helvetica", 8)
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    # canvas.rotate(45)

    canvas.restoreState()


def run_rawsql_data(request, sql, cs=0):
    """
    Method to handle Database connections
    User Reporting DB for reporting but
    Fallback to Transaction DB if any error
    """
    try:
        db_inst = 'default'
        dbinstance = connections[db_inst]
        print('Query Reporting database .....')
        with dbinstance.cursor() as cursor:
            cursor.execute(sql)
            # pd.read_sql_query(sql, cursor)
            desc = cursor.description
            data = cursor.fetchall()
    except Exception as e:
        print('Defaulting to Transaction DB - %s' % (str(e)))
        with connection.cursor() as cursor:
            cursor.execute(sql)
            desc = cursor.description
            data = cursor.fetchall()
        return data, desc
    else:
        return data, desc


def get_data(report_id, params={}):
    """Method to get data from sql."""
    try:
        dtf = ''
        if params and 'start_date' in params and 'end_date' in params:
            s_date = params['start_date']
            e_date = params['end_date']
            dtf = "WHERE ocr.date_case_opened "
            dtf += "between '%s' AND '%s' " % (s_date, e_date)
        sql = "select rou.id, "
        sql += "concat(po.id, ' : ', po.org_unit_name) as parent_unit, "
        sql += "concat(rou.id, ' : ', rou.org_unit_name) as org_unit_name, "
        sql += "rou.org_unit_type_id, SUM(COALESCE(u.cases, 0)) as cases, "
        sql += "1 as ovccount, 0 as org_unit "
        sql += "from reg_org_unit rou "
        sql += "inner join reg_org_unit po on po.id=rou.parent_org_unit_id "
        sql += "left join ( select report_orgunit_id as unit_id, "
        sql += "count(report_orgunit_id) as cases from ovc_case_geo "
        sql += "inner join ovc_case_record ocr ON ocr.case_id=case_id_id "
        sql += "%s" % (dtf)
        sql += "group by report_orgunit_id) as u on u.unit_id = rou.id "
        sql += "where rou.is_void = False and rou.org_unit_type_id in "
        sql += "('TNGD', 'TNGP', 'TNRH', 'TNAP', 'TNRS', 'TNRR', 'TNRB') "
        sql += "group by u.cases, rou.id, rou.org_unit_name, po.id, "
        sql += "po.org_unit_name order by rou.parent_org_unit_id ASC"
        # df = pd.DataFrame(list(qs.values('parent_org_unit_id',
        # 'org_unit_name', 'ovccount')))
        data, cols = run_rawsql_data(None, sql)
        columns = [col[0] for col in cols]
        # print('cols', columns)
        df = pd.DataFrame(data)
        results = df.values.tolist()
        # fdata = [columns] + results
        ndf = pd.DataFrame(results, columns=columns).fillna(0)
        idx = ['parent_unit', 'org_unit_name']
        cols = []
        table = pd.pivot_table(ndf, values='cases', index=idx,
                               columns=cols, aggfunc=sum,
                               fill_value=0, margins=True,
                               margins_name='Grand Total')
    except Exception as e:
        print('Error getting data - %s' % (str(e)))
        return None
    else:
        return table


def write_register(response, file_name, params={}):
    """Method to write to pdf from pandas."""
    try:

        # datas = pd.DataFrame(data)
        # response = '%s.pdf' % (file_name)
        STATIC_ROOT = settings.STATICFILES_DIRS[0]
        rparams = file_name.split('_')
        rid = int(rparams[3])
        region = rparams[0].replace('-', ' ')
        report_name = rparams[1].replace('-', ' ')
        if 'OU ' in region or 'ou_name' in params:
            ou_name = params['ou_name'] if 'ou_name' in params else 'DCS'
            report_name = "%s (%s)" % (report_name, ou_name)
        if rid == 6:
            report_name = 'CP Status Report'
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Data', alignment=TA_LEFT, fontSize=8,
            leading=11, fontColor='#FFFFFF'))
        styles.add(ParagraphStyle(
            name='Line_Data_Small', alignment=TA_LEFT,
            fontSize=7, leading=8))
        styles.add(ParagraphStyle(
            name='Line_Data_Large', alignment=TA_LEFT,
            fontSize=12, leading=15))
        styles.add(ParagraphStyle(
            name='Line_Data_Largest', alignment=TA_LEFT,
            fontSize=14, leading=15))
        styles.add(ParagraphStyle(
            name='Line_Label', font='Helvetica-Bold',
            fontSize=7, leading=6, alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Label1', font='Helvetica-Bold', fontSize=7,
            leading=6, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(
            name='Line_Label_Center', font='Helvetica-Bold',
            fontSize=12, alignment=TA_CENTER))
        element = []
        datenow = datetime.now()
        tarehe = datenow.strftime("%d, %b %Y %I:%M %p")
        url = 'https://childprotection.go.ke'
        # ous = get_data(rid)
        # col_size = len(df.columns)
        # dt_size = len(df.index)
        # Handle headers
        address = '<b>MINISTRY OF PUBLIC SERVICE, GENDER, SENIOR CITIZENS'
        address += " AFFAIRS & SPECIAL PROGRAMMES"
        address += "<br />STATE DEPARTMENT FOR SOCIAL PROTECTION,"
        address += " SENIOR CITIZENS AFFAIRS & SPECIAL PROGRAMMES"
        address += "<br />DIRECTORATE OF CHILDREN'S SERVICES</b>"
        report_number = '%s\n%s CPIMS Report\n%s' % (url, report_name, tarehe)
        # Work on the data
        start_date = ''
        end_date = datenow.strftime("%d, %B %Y")
        mon = int(datenow.strftime("%m"))
        year = int(datenow.strftime("%Y"))
        fyear = year - 1 if mon < 7 else year
        if rid in [1, 2, 4]:
            start_date = '1, July %s to ' % (fyear)
        if params and 'start_date' in params and 'end_date' in params:
            start_date = params['start_date']
            end_date = ' to %s' % params['end_date']
        dates = '%s%s' % (start_date, end_date)
        bar_code = BarCode(value='%s' % (report_number))
        # Logo
        logo = "%s/img/logo_gok.png" % (STATIC_ROOT)
        sd = Image(logo)
        sd.drawHeight = 0.6 * inch
        sd.drawWidth = 0.7 * inch
        data1 = [[sd, Paragraph(address, styles["Line_Data_Large"]),
                  bar_code], ['', '', Paragraph(dates, styles["Line_Label"])]]
        tt = Table(
            data1, colWidths=(2.1 * cm, None, 3.8 * cm,),
            rowHeights=(1.75 * cm, .5 * cm,))

        tt.setStyle(TableStyle([
            ('INNERGRID', (2, 1), (2, 2), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (2, 3), (-1, -1), 'RIGHT'),
        ]))
        rnote = '<b>NOTE: This is a computer generated report <br /> '
        rnote += ' as at %s.</b>' % (tarehe)
        element.append(tt)
        element.append(Spacer(0.1 * cm, .2 * cm))
        data1 = [[Paragraph('Report<br />Name:', styles["Line_Label"]),
                  Paragraph(report_name, styles["Line_Data_Largest"]),
                  Paragraph(rnote, styles["Line_Data_Small"]), ]]

        t0 = Table(data1, colWidths=(2 * cm, None, 6.1 * cm,))
        t0.setStyle(TableStyle([
            ('INNERGRID', (1, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        element.append(t0)
        # Configure columns
        qstyle = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('SPAN', (0, 0), (-1, 0)),
             ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
             ('ALIGN', (2, 2), (-1, -1), 'RIGHT'),
             ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])

        element.append(Spacer(0.1 * cm, .6 * cm))
        # Get the data ready for reportlab
        mdt = get_data(6, params)
        print('mdt', mdt)
        qdsize = 0
        if mdt.empty:
            qa_values = []
            # print(qa_values)
            dtitle = "DQA Records for your action"
            colw = (2.86 * cm, 16.4 * cm)
            qdata = ["", "No records Found matching your query. "]
            dq_data = [[dtitle, ""], qdata]
            dq_data += qa_values
        else:
            colw = (6.86 * cm, 10.4 * cm, 2 * cm)
            # dq_data = [["CPIMS Status Report", ""], qdata]
            # mdt_values = dq_data + mdt.reset_index().values.tolist()
            # mdt_values = dq_data + list(mdt.reset_index().columns.values)
            mdt_names = list(mdt.reset_index().columns.values)
            mdt_values = mdt.reset_index().values.tolist()
            ndt = []
            dts = []
            for dt in mdt_values:
                # print(dt)
                dt[1] = Paragraph(dt[1], styles["Line_Data"])
                dt[2] = '{:20,.0f}'.format(dt[2])
                if dt[0] not in dts:
                    dts.append(dt[0])
                    dt[0] = Paragraph(dt[0], styles["Line_Data"])
                else:
                    dt[0] = ''
                ndt.append(dt)
            dqs_data = [["CPIMS Status Report", "", ""], mdt_names]
            dq_data = dqs_data + ndt
        t3 = Table(dq_data, colWidths=colw, repeatRows=2)
        t3.setStyle(qstyle)
        element.append(t3)
        element.append(Spacer(0.1 * cm, .5 * cm))
        ftxt = TXT[4]
        footer = Paragraph(ftxt % (qdsize), styles["Line_Data_Small"])
        element.append(footer)
        # end other reports
        doc = SimpleDocTemplate(
            response, pagesize=A4, rightMargin=20,
            leftMargin=20, topMargin=30, bottomMargin=30,
            keywords="CPIMS, Child Protection in Kenya, UNICEF, DCS, <!NMA!>")
        doc.pagesize = portrait(A4)
        # doc.build(element)
        cpims_txt = 'Child Protection Information Management System (CPIMS)'
        doc.fund_name = ''
        doc.watermark = ''
        doc.report_info = ''
        doc.source = cpims_txt
        doc.build(element, onFirstPage=draw_page, onLaterPages=draw_page,
                  canvasmaker=Canvas)
    except Exception as e:
        print('Error generating pdf - %s' % (e))
    else:
        pass


def write_document(response, file_name, params={}):
    """Method to write to pdf from pandas."""
    try:

        # datas = pd.DataFrame(data)
        # response = '%s.pdf' % (file_name)
        STATIC_ROOT = settings.STATICFILES_DIRS[0]
        rparams = file_name.split('_')
        print('params', rparams, params)
        rid = int(rparams[3])
        region = rparams[0].replace('-', ' ')
        report_name = rparams[1].replace('-', ' ')
        if 'OU ' in region or 'ou_name' in params:
            ou_name = params['ou_name'] if 'ou_name' in params else 'DCS'
            report_name = "%s (%s)" % (report_name, ou_name)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Data', alignment=TA_LEFT, fontSize=8,
            leading=11, fontColor='#FFFFFF'))
        styles.add(ParagraphStyle(
            name='Line_Data_Small', alignment=TA_LEFT,
            fontSize=7, leading=8))
        styles.add(ParagraphStyle(
            name='Line_Data_Large', alignment=TA_LEFT,
            fontSize=12, leading=15))
        styles.add(ParagraphStyle(
            name='Line_Data_Largest', alignment=TA_LEFT,
            fontSize=14, leading=15))
        styles.add(ParagraphStyle(
            name='Line_Label', font='Helvetica-Bold',
            fontSize=7, leading=6, alignment=TA_LEFT))
        styles.add(ParagraphStyle(
            name='Line_Label1', font='Helvetica-Bold', fontSize=7,
            leading=6, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(
            name='Line_Label_Center', font='Helvetica-Bold',
            fontSize=12, alignment=TA_CENTER))
        element = []
        datenow = datetime.now()
        tarehe = datenow.strftime("%d, %b %Y %I:%M %p")
        url = 'https://childprotection.go.ke'
        # ous = get_data(rid)
        # col_size = len(df.columns)
        # dt_size = len(df.index)
        # Handle headers
        address = '<b>MINISTRY OF PUBLIC SERVICE, GENDER, SENIOR CITIZENS'
        address += " AFFAIRS & SPECIAL PROGRAMMES"
        address += "<br />STATE DEPARTMENT FOR SOCIAL PROTECTION,"
        address += " SENIOR CITIZENS AFFAIRS & SPECIAL PROGRAMMES"
        address += "<br />DIRECTORATE OF CHILDREN'S SERVICES</b>"
        report_number = '%s\n%s CPIMS Report\n%s' % (url, report_name, tarehe)
        # Work on the data
        start_date = ''
        end_date = datenow.strftime("%d, %B %Y")
        mon = int(datenow.strftime("%m"))
        year = int(datenow.strftime("%Y"))
        fyear = year - 1 if mon < 7 else year
        if rid in [1, 2, 4]:
            start_date = '1, July %s to ' % (fyear)
        dates = '%s%s' % (start_date, end_date)
        bar_code = BarCode(value='%s' % (report_number))
        # Logo
        logo = "%s/img/logo_gok.png" % (STATIC_ROOT)
        sd = Image(logo)
        sd.drawHeight = 0.6 * inch
        sd.drawWidth = 0.7 * inch
        data1 = [[sd, Paragraph(address, styles["Line_Data_Large"]),
                  Paragraph('CPIMS %s Report' % (region),
                            styles["Line_Data_Large"]), bar_code],
                 ['', '', Paragraph(dates,
                                    styles["Line_Label"]), '']]
        tt = Table(
            data1, colWidths=(2.1 * cm, None, 5.9 * cm, 3.4 * cm,),
            rowHeights=(1.2 * cm, .5 * cm,))

        tt.setStyle(TableStyle([
            ('INNERGRID', (2, 0), (2, 1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        rnote = '<b>NOTE: This is a computer generated report <br /> '
        rnote += ' as at %s.</b>' % (tarehe)
        element.append(tt)
        element.append(Spacer(0.1 * cm, .2 * cm))
        data1 = [[Paragraph('Report<br />Name:', styles["Line_Label"]),
                  Paragraph(report_name, styles["Line_Data_Largest"]),
                  Paragraph(rnote, styles["Line_Data_Small"]), ]]

        t0 = Table(data1, colWidths=(2 * cm, None, 6.1 * cm,))
        t0.setStyle(TableStyle([
            ('INNERGRID', (1, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        element.append(t0)
        # print(type(col_size), col_size)
        style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('ALIGN', (2, 3), (-1, -1), 'RIGHT'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        # Configure columns
        flts = 0
        cols, idx = get_pivot_vars(rid)
        # print(len(cols), len(idx), cols, idx)
        mflts = {}
        ou_id = params['ou_id'] if 'ou_id' in params else 0
        if rid == 4:
            mflts = {'ou_id': ou_id}
        dfs, odf = create_pivot(rid, idx, cols, flts, mflts)
        # datas = np.vstack((list(dfs), np.array(dfs))).tolist()
        dt_size = len(dfs.index)
        col_size = len(dfs.columns)
        hdx = len(idx)
        rdx = len(cols)
        print('Size of Index / Columns', dt_size, col_size)
        # Now prepare the data
        if col_size > 2:
            pvt_names = list(dfs.reset_index().columns.names)
            dcols = {}
            dsize = len(dfs.columns.values)
            pvt_values = list(dfs.reset_index().columns.values)
            hd_len = len(pvt_names)
            # titles = list(pvt_values[0]) + pvt_names
            col_length = 0
            for col in pvt_values:
                col_length = len(col)
                break
            for i in range(0, col_length):
                for col in pvt_values:
                    if i not in dcols:
                        dcols[i] = [col[i]]
                    else:
                        dcols[i].append(col[i])
            fcls = []
            for fc in dcols:
                fl = dcols[fc]
                if fc == 0:
                    fcl = list(dict.fromkeys(fl))
                    nfcl = fcl + [''] * (len(fl) - len(fcl))
                    fcls.append(nfcl)
                else:
                    fcls.append(fl)
            data_list = dfs.reset_index().values.tolist()
            # data_list = [dfs.columns.values.tolist()] + dfs.values.tolist()
            # print(data_list)
            dtl, dd = [], []
            for dl in data_list:
                # dl[1] = Paragraph(dl[1], styles["Normal"])
                if dl[0] not in dd:
                    dd.append(dl[0])
                    # dl[0] = Paragraph(dl[0], styles["Normal"])
                    dtl.append(dl)
                else:
                    dl[0] = ''
                    dtl.append(dl)

            datas = fcls + dtl
            cols = get_rlcols(rid, dsize)
            # Create table style
            bs = col_size + (hdx - 1)
            ds = dt_size + (rdx)
            style = TableStyle(
                [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                 ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                 ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                 ('ALIGN', (hdx, hd_len), (-1, -1), 'RIGHT'),
                 # ('FONTSIZE', (0, 0), (-1, -1), 9),
                 ('FONTNAME', (0, ds), (-1, -1), 'Helvetica-Bold'),
                 ('FONTNAME', (bs, 0), (-1, -1), 'Helvetica-Bold'),
                 ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])

            t1 = Table(datas, colWidths=cols, repeatRows=hd_len)
            t1.setStyle(style)
            element.append(t1)
        else:
            ftxt = TXT[3]
            bfooter = Paragraph(ftxt, styles["Line_Data_Largest"])
            element.append(Spacer(0.1 * cm, 1.1 * cm))
            element.append(bfooter)
        qstyle = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('SPAN', (0, 0), (-1, 0)),
             ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
             ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
             ('BACKGROUND', (0, 0), (-1, 0), '#89CFF0')])
        element.append(Spacer(0.1 * cm, 1.5 * cm))
        if rid == 4 and col_size > 2:
            # Add case management details
            cmdts = get_cm(rid, ou_id)
            cmsize = len(cmdts.index)
            cmgt = "This Week's Summons, Court Sessions and Discharges"
            if cmsize > 0:
                cm_values = cmdts.values.tolist()
                colw = (2.86 * cm, 4.0 * cm, 1.0 * cm, 5.0 * cm,
                        6.0 * cm, 6.0 * cm, 3.0 * cm)
                data = ["CPIMS ID", "Name / Initials", "Age", "DoB",
                        "Case Category", "Case Management", "Due Date"]
                cm_data = [[cmgt, "", "", "", "", "", ""], data]
                cm_data += cm_values
            else:
                colw = (2.86 * cm, 25.0 * cm)
                data = ["", "No data available from the System."]
                cm_data = [[cmgt, ""], data]

            t2 = Table(cm_data, colWidths=colw, repeatRows=2)
            t2.setStyle(qstyle)
            element.append(t2)
            element.append(Spacer(0.1 * cm, .5 * cm))
            ftxt = TXT[1]
            footer = Paragraph(ftxt % (cmsize), styles["Line_Data_Small"])
            element.append(footer)
            element.append(Spacer(0.1 * cm, .6 * cm))
            # Also add DQA details
            qdts = get_dqa(odf)
            qdsize = len(qdts.index)
            if qdsize > 0:
                qa_values = qdts.values.tolist()
                # print(qa_values)
                dtitle = "DQA Records for your action"
                colw = (2.86 * cm, 4.0 * cm, 1.0 * cm, 5.0 * cm, 3.0 * cm,
                        3.0 * cm, 3.0 * cm, 3.0 * cm, 3.0 * cm)
                qdata = ["CPIMS ID", "Name / Initials", "Age",
                         "Case Category", "DQA Sex", "DQA DoB",
                         "DQA Age", "Case Status", "Case Date"]
                dq_data = [[dtitle, "", "", "", "", "", "", "", ""], qdata]
                dq_data += qa_values
            else:
                colw = (2.86 * cm, 25.0 * cm)
                qdata = ["", "No data available from the System."]
                dq_data = [["DQA Records for your action", ""], qdata]
            t3 = Table(dq_data, colWidths=colw, repeatRows=2)
            t3.setStyle(qstyle)
            element.append(t3)
            element.append(Spacer(0.1 * cm, .5 * cm))
            ftxt = TXT[2]
            footer = Paragraph(ftxt % (qdsize), styles["Line_Data_Small"])
            element.append(footer)
        doc = SimpleDocTemplate(
            response, pagesize=A4, rightMargin=20,
            leftMargin=20, topMargin=30, bottomMargin=30,
            keywords="CPIMS, Child Protection in Kenya, UNICEF, DCS, <!NMA!>")
        doc.pagesize = landscape(A4)
        # doc.build(element)
        doc.watermark = 'CPIMS'
        doc.fund_name = ''
        doc.report_info = ''
        doc.source = 'Child Protection Information Management System (CPIMS)'
        doc.build(element, onFirstPage=draw_page, onLaterPages=draw_page,
                  canvasmaker=Canvas)
    except Exception as e:
        print('Error generating pdf - %s' % (e))
    else:
        pass


def get_dqa(df):
    """Method to get DQA issues."""
    try:
        df0 = df[(df.dob == '') | (df.dqa_sex != 'OK') |
                 (df.dqa_age != 'OK') | (df.case_status == 'Pending')]
        df1 = df0[['cpims_id', 'child_names', 'age', 'case_category',
                   'dqa_sex', 'dqa_dob', 'dqa_age', 'case_status',
                   'case_date']].drop_duplicates()
        # print(df1)
    except Exception as e:
        print('Error getting data frame - %s' % (e))
        brdf = Blank()
        brdf.index = []
        return brdf
    else:
        return df1


def get_cm(rid, ou_id):
    """Method to get case management details."""
    try:
        cpdata = 'CMSC'
        if rid in [5]:
            cpdata = 'CMSI'
        file_name = '/dbs/CPIMSDATA-%s.csv' % (cpdata)
        df = pd.read_csv(file_name, na_filter=False)
        df0 = df[(df.ou_id == ou_id)]
        df1 = df0[['cpims_id', 'child_names', 'age', 'dob', 'case_category',
                   'case_status', 'due_date']].drop_duplicates()
    except Exception as e:
        print('Error getting case management data - %s' % (e))
        brdf = Blank()
        brdf.index = []
        return brdf
    else:
        return df1


def create_pivot(rid, idx, cols, flts, filters={}):
    """Method to create pivot data."""
    try:
        cpdata = 'FY'
        if rid in [3]:
            cpdata = 'SI'
        file_name = '/dbs/CPIMSDATA-%s.csv' % (cpdata)
        df = pd.read_csv(file_name, na_filter=False)
        if flts:
            # (df.cc_id == 'CDIS') &
            df = df[(df.county_id == flts)]
        if rid == 4:
            if 'ou_id' in filters:
                ou_id = filters['ou_id']
                df = df[(df.ou_id == ou_id)]
        table = pd.pivot_table(df, index=idx, columns=cols,
                               values=["ovccount"],
                               margins=True, margins_name='Total',
                               aggfunc=sum, fill_value=0)
        # table.query('"case category" == ["Abandoned"]')
    except Exception as e:
        print("Error or NO data in pivot - %s" % (e))
        brdf = Blank()
        brdf.index = []
        return brdf, brdf
    else:
        return table, df


def get_pivot_vars(rid):
    """Method to get pivot variables."""
    try:
        if rid == 1:
            cols = ["case_year", "case_month"]
            idx = ["county", "sub_county", "org_unit"]
        elif rid == 3:
            cols = ["sex"]
            idx = ["unit_type", "org_unit"]
        else:
            cols = ["agerange", "sex"]
            idx = ["case_category"]
    except Exception as e:
        raise e
    else:
        return cols, idx


def get_rlcols(rid, dsize):
    """Method to get report lab cols."""
    try:
        d0 = 27.86 - ((1.5 * dsize) + 2.7 + 4.1)
        cols = tuple([2.7 * cm, 4.1 * cm, d0 * cm] + [1.5 * cm] * (dsize))
        if rid in [2, 4]:
            d0 = 27.86 - ((2.0 * dsize))
            cols = tuple([d0 * cm] + [2.0 * cm] * (dsize))
        if rid in [3]:
            d0 = 27.86 - ((2.5 * dsize) + 4.5)
            cols = tuple([4.5 * cm, d0 * cm] + [2.5 * cm] * (dsize))
    except Exception as e:
        raise e
    else:
        return cols


def get_register(request, id=1):
    """Download without printing."""
    # fname = 'test.pdf'
    datenow = datetime.now()
    tarehe = datenow.strftime("%Y%M%d")
    fn = 'Org-Unit_Case-Load-Data-Quality'
    report_id = 4
    f_name = "%s_%s_%s" % (fn, tarehe, report_id)
    fname = "%s.pdf" % (f_name)
    # create_document(buffer, pd)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % (fname)
    # Params
    params = {'name': 'Case Load & Data Quality', 'ou_id': 19,
              'ou_name': 'KASARANI SUB COUNTY CHILDREN OFFICE'}
    write_document(response, f_name, params)

    '''

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    '''
    return response
