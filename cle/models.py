from django.db import models

class Cle(models.Model):
    nom=models.CharField(max_length=100)

    class Meta:
        verbose_name='cle'
        ordering=['nom']

class Espece(models.Model):
    nom=models.CharField(max_length=100)
    nom_latin=models.CharField(max_length=100)
    description=models.CharField(max_length=2000)
    cle_name=models.ForeignKey(Cle, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Espece'
        ordering=['nom']

class Caractere (models.Model):
    nom=models.CharField(max_length=100)
    
    class Meta:
        verbose_name='Caractere'
        ordering=['id']

    def __str__(self):
        return self.nom

class Etat_caracteres(models.Model):
    etat=models.CharField(max_length=100)
    caractere=models.ForeignKey(Caractere, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Etat de Caractere'

    def __str__(self):
        return self.etat

class Espece_caractere(models.Model):
    espece=models.ForeignKey(Espece, on_delete=models.CASCADE)
    caractere=models.ForeignKey(Caractere, on_delete=models.CASCADE)
    etat=models.CharField(max_length=100)
