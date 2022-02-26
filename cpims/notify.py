import io
from datetime import datetime
from documents import write_document, run_query
from emails import send_email
from queries import QUERY

RN = {}
RN[1] = 'National_Case-Load-by-County'
RN[2] = 'National_Case-Load-by-Case-categories'
RN[3] = 'National_Statutory-Institution-Population'
RN[4] = 'Sub-County_Case-Load'
RN[5] = 'Institution_Population'


def prepare_data(report_id, pd):
    """Method to prepare data for sending."""
    try:
        buffer = io.BytesIO()
        datenow = datetime.now()
        tarehe = datenow.strftime("%Y%M%d")
        dfn = "National_Case-Load-by-County"
        fn = RN[report_id] if report_id in RN else dfn
        fname = "%s_%s_%s" % (fn, tarehe, report_id)
        mc_name = "%s.pdf" % (fname)
        report_name = pd['name']
        # create_document(buffer, pd)
        write_document(buffer, fname, pd)
        pdf = buffer.getvalue()
        buffer.close()
        intro = '%s case load report' % (report_name)
        sign = 'Deparment of Children Services (DCS)'
        sign_txt = 'Quality Data for Child Protection'
        hmsg = '%s<table width="90%%"></table>' % (intro)
        fs = 'style="width:60%; float: left; text-align: right;"'
        vs = 'style="width:30%; float: right; text-align: right;"'
        hmsg = hmsg.replace('class="field"', fs)
        hmsg = hmsg.replace('class="value"', vs)
        hmsg = hmsg.replace('<i class="fa fa-usd"></i>', 'USD')
        hmsg = hmsg.replace(
            'class="cart-total text-center"', 'align="right"')
        # hmsg = hmsg.decode('utf-8', 'ignore')
        hmsg += '<br/><p>%s<br/><i>%s</i></>' % (sign, sign_txt)
        params = {'subject': "CPIMS Data Notification",
                  'attachment': pdf, 'doc': mc_name,
                  'html': hmsg}
    except Exception as e:
        print('Error preparing data %s' % str(e))
    else:
        return params


def get_users(uid=1, dl=0):
    """Method to get county coordinators emails."""
    try:
        emails = []
        sql = QUERY[uid]
        df = run_query(sql)
        data = df.values.tolist()
        for dt in data:
            val = dt[0]
            if dl > 0:
                val = {dt[0]: dt[1]}
            emails.append(val)
    except Exception as e:
        raise e
    else:
        return emails


def get_contacts(report_id):
    """Method to get contacts to notify."""
    try:
        emails = ["nmugaya@gmail.com"]
        gok = ["sochieng2002@gmail.com", "ogindo.p@gmail.com",
               "polycarp.otieno@gmail.com", "jmugah@healthit.uonbi.ac.ke",
               "polycarp.otieno@thepalladiumgroup.com"]
        sections = ["strategicinterventiondcs@gmail.com",
                    "countertraffickingkenya@gmail.com",
                    "communitychild2017@gmail.com",
                    "childprotectiondivision@gmail.com"]
        if report_id in [1, 2]:
            # case load by county + by category + SI Pop
            emails += gok
            # emails = emails
        if report_id in [2]:
            emails += sections
        if report_id in [1]:
            # case load by county
            # ccc_emails = get_users()
            # emails += ccc_emails
            scco_emails = get_users(3)
            emails = scco_emails
        if report_id in [3]:
            emails += ["kabuagi@gmail.com"]
        # emails.append("nmugaya@gmail.com")
    except Exception as e:
        raise e
    else:
        return emails


def notices(report_name):
    """Method to process different notifications."""
    try:
        hm, tm = None, None
        datenow = datetime.now()
        tarehe = int(datenow.strftime("%d"))
        dow = str(datenow.strftime("%a"))
        idow = ['Mon', 'Sat', 'Sun']
        print(dow, tarehe)
        if report_name == 'hourly':
            report_id = 0
            pd = {'name': report_name.title()}
            params = prepare_data(report_id, pd)
            hm = params['html']
        elif report_name == 'daily' and dow not in idow and tarehe != 1:
            report_id = 4
            pd = {'name': report_name.title(), 'ou_id': 19,
                  'ou_name': 'KASARANI SUB COUNTY CHILDREN OFFICE'}
            params = prepare_data(report_id, pd)
            hm = params['html']
        elif report_name == 'weekly' and tarehe > 7:
            # Institution Report to also be sent on Monday
            report_id = 3
            pd = {'name': report_name.title()}
            params = prepare_data(report_id, pd)
            hm = params['html']
        elif report_name == 'monthly':
            report_id = 1
            pd = {'name': report_name.title()}
            params = prepare_data(report_id, pd)
            hm = params['html']

        if hm:
            emails = get_contacts(report_id)
            for email in emails:
                send_email(email, tm, hm, params)
    except Exception as e:
        raise e
    else:
        pass


if __name__ == '__main__':
    # gu = get_users(uid=3, dl=1)
    # print(gu)
    pass
