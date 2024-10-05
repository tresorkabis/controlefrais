from django.contrib import admin
from frais.models import *
from etudiant.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors 
from etudiant.admin import controlesite

from django.http import HttpResponse
from django.utils.html import format_html

def download_pdf(self, request, queryset):
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('Liste des Frais')
    pdf.drawString(50, 700, "Liste des Frais")

    ordered_queryset = queryset.order_by('code')

    headers = [field.verbose_name for field in self.model._meta.fields]
    data = [headers]

    for obj in queryset:
        data_row = [str(getattr(obj, field.name)) for field in self.model._meta.fields]
        data.append(data_row)

    table = Table(data)
    table.setStyle(TableStyle(
        [
        ('BACKGROUND', (0,0),(-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black)   
        ]    
    ))

    canvas_width = 600
    canvas_height = 600

    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 40, canvas_height - len(data))

    pdf.save()
    return response 

download_pdf.short_description = "Liste des frais selectionnées en pdf."    

class FraisAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'libelle',
        'motantpayer'
    )
    
    actions = [download_pdf]

controlesite.register(Frais, FraisAdmin)

class PayementAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:80px; max-height:80px"/>'.format(obj.qrcode.url))
    image_tag.short_description = "QR Code"
    list_display = (
        'id',
        'eleve',
        'datepayement',
        'motantpaye',
        'image_tag'
    )
    ordering = ('id',)
controlesite.register(Payement, PayementAdmin)



