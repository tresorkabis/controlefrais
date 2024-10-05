from django.db import models
from etudiant.models import Eleve

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
    motantpayer = models.IntegerField()

    def __str__(self):
        return str(self.id) + "-" + self.eleve.nom + "-"+self.frais.libelle 
