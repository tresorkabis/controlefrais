from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class Section(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    libelle = models.CharField(max_length=50)

    def __str__(self):
        return self.libelle 

class Classe(models.Model):
    code = models.CharField(max_length=10, primary_key=True) 
    libelle = models.CharField(max_length=50)

    def __str__(self):
        return self.libelle

class Eleve(models.Model):     
    matricule = models.CharField(max_length=10, primary_key=True, verbose_name="MATRICULE")
    nom = models.CharField(max_length=50, verbose_name="NOM")
    postnom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=1)
    adresse = models.CharField(max_length=100)
    datenaissance = models.DateField()
    lieunaissance = models.CharField(max_length=50)
    nomtutaire = models.CharField(max_length=100)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to="qrcode/", null=True, blank=True)

    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        ct = self.matricule + "-" + self.nom + "-" + self.classe.libelle 
        qr = qrcode.make(ct)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file = File(buffer, name=self.nom+".png")
        self.qrcode = file 
        super(Eleve, self).save(*args, **kwargs)
    