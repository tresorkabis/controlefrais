from io import BytesIO
from django.db import models
import qrcode
from etudiant.models import Eleve
from django.core.files import File

class Frais(models.Model):
    code = models.CharField(max_length=10, primary_key=True, verbose_name="CODE")
    motantpayer = models.IntegerField()
    libelle = models.CharField(max_length=50, default="Frais")

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name_plural = "Frais" 

class Payement(models.Model):
    frais = models.ForeignKey(Frais, on_delete=models.CASCADE)
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    datepayement = models.DateField()
    motantpaye = models.IntegerField()
    qrcode = models.ImageField(upload_to="qrcode/", null=True, blank=True)

    def __str__(self):
        return str(self.id) + "-" + self.eleve.nom + "-"+self.frais.libelle 
    
    def save(self, *args, **kwargs):
        ps = Payement.objects.filter(eleve__matricule=self.eleve.matricule)
        montant = self.motantpaye
        for p in ps:
            if p.frais.code == "001":
                montant = montant + p.motantpaye
        ct = self.eleve.matricule + "-" + self.eleve.nom + "-" + self.eleve.classe.libelle + "/" + str(montant) 
        qr = qrcode.make(ct)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        name = str(self.datepayement)+"-"+self.eleve.nom+".png"
        file = File(buffer, name=name)
        self.qrcode = file 
        super(Payement, self).save(*args, **kwargs)