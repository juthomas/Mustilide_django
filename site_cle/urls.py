from django.contrib import admin
from django.urls import path, include
from cle.views import accueil, affiche_liste, affiche_ajouter, affiche_specialiste, affiche_contact
from cle.views import affiche_europe, affiche_amerique, espece, caractere, cle_en_cours



urlpatterns = [
    path('home',accueil, name='index'),
    path('liste', affiche_liste, name='afficheliste'),
    path('ajouter', affiche_ajouter, name='afficheajouter'),
    path('account/', include("cle.urls")),
    path('specialiste', affiche_specialiste, name='affichespecialiste'),
    path('contact', affiche_contact, name='affichecontact'),
    path('ceurope', affiche_europe, name='afficheeurope'),
    path('camerique', affiche_amerique, name='afficheamerique'),
    path('afficher/espece/<int:id_espece>', espece, name='affiche_espece'),
    path('afficher/caractere/<int:id_caractere>', caractere, name='afficher_caractere'),
    path('cle/en-cours/<int:id_etat>', cle_en_cours, name="cle_en_cours")
 
]
