from io import BytesIO
# from django.http import HttpResponse
from django.template.loader import get_template,render_to_string

from xhtml2pdf import pisa
# import logging
import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.conf import settings
import json

def get_recipient_model():
    """
    Returns the Recipient model that is active in this project.
    """
    path = getattr(settings, 'RECIPIENT_MODEL')
    try:
        return django_apps.get_model(path)
        # print(django_apps.get_model(path).Meta.verbose_name)
    except ValueError:
        raise ImproperlyConfigured(
            "path must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "path refers to model that\
             has not been installed"
        )


def SendMail(subject='', message_body='', sender='', recipient_list=[], attachment_list=[], template_data={}, is_html_msg=True):
    if template_data:
        html_body = render_to_string(template_data.path, template_data.context)
        text_body = strip_tags(html_body)
        is_html_msg = True
    elif is_html_msg:
        html_body = message_body
        text_body = strip_tags(message_body)
    else:
        text_body = message_body
    if sender == '':
        msg = EmailMultiAlternatives(
            subject=subject, body=text_body, to=recipient_list)
    else:
        msg = EmailMultiAlternatives(
            subject, text_body, sender, recipient_list,reply_to=[sender])
    if is_html_msg:
        msg.attach_alternative(html_body, "text/html")
    for x in attachment_list:
        msg.attach(x["name"], x["content"], x["content_type"])
    msg.send(fail_silently=False)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue() #HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def render_filter_obj(fObj, qObj):
    query = []
    # logging.error(fObj)
    # logging.error(qObj)
    for v in fObj:
        if isinstance(v['title'], list):
            for vx in v['title']:
                if qObj.__contains__(vx['name']):
                    query.append(
                        {'title': vx['title'], 'value': qObj[vx['name']]})
        else:
            if qObj.__contains__(v['name']):
                flg = False
                if 'type' in v.keys():
                    if v['type'] =='date':
                        flg = True
                        query.append({'title': v['title'], 'value': datetime.datetime.strptime(qObj[v['name']], '%Y-%m-%d').strftime('%d/%m/%Y')})
                if not flg:
                    query.append({'title': v['title'], 'value': qObj[v['name']]})
            elif qObj.__contains__('filter{' + v['name'] + '.gte}'):
                if 'type' in v.keys():
                    if v['type'] =='period':
                        query.append({'title': v['title'], 'value': datetime.datetime.strptime(qObj['filter{' + v['name'] + '.gte}'], '%Y-%m-%d').strftime('%d/%m/%Y') + ' To ' + datetime.datetime.strptime(qObj['filter{' + v['name'] + '.lte}'],'%Y-%m-%d').strftime('%d/%m/%Y')})

    # logging.error(query)
    return query


def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == 'body':
            return box

        return get_page_body(box.all_children())

def runSQLQuery(sql,returnJson=False):
    cursor = connection.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    data = [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]
    if returnJson:
        return json.dumps(data)
    return data