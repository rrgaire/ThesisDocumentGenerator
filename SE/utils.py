from io import BytesIO
from django.http import HttpResponse
from mailmerge import MailMerge
from datetime import date
from django.shortcuts import render
import sys
import os

#from django.template.loader import get_template


def render_to_word(template_src: object, doc_name: object, context_dict: object = {}) -> object:
    document = MailMerge(template_src)
    document.merge_pages([context_dict,])
    document.write(doc_name)


def make_table(template_src: object, doc_name: object, context_dict: object) -> object:
    document = MailMerge(template_src)
    document.merge(**context_dict)
    document.merge_rows('name', context_dict['list'])
    document.write(doc_name)

