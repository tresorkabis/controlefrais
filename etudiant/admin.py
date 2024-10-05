from django.contrib import admin
from .models import *

admin.site.register(Section)
admin.site.register(Classe)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors 

from django.http import HttpResponse
from django.utils.html import format_html

def download_eleve_pdf(self, request, queryset):
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('Liste des élèves')
    pdf.drawString(50, 700, "Liste des élèves")

    ordered_queryset = queryset.order_by('matricule')

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

download_eleve_pdf.short_description = "Liste des élèves selectionnées en pdf."

class EleveAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:80px; max-height:80px"/>'.format(obj.qrcode.url))
    image_tag.short_description = "QR Code"
    list_display = (
        'matricule',
        'nom',
        'postnom',
        'prenom',
        'sexe',
        'nomtutaire',
        'classe',
        'image_tag'
    )
    ordering = ('matricule',)
    
    actions = [download_eleve_pdf]

admin.site.register(Eleve, EleveAdmin)