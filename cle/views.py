from django.shortcuts import render,redirect
from datetime import datetime
from collections import Counter
from django.core.mail import send_mail
from cle.models import Espece, Caractere, Etat_caracteres, Espece_caractere

def accueil(request):
	date_du_jour = datetime.now()
	date_du_jour_txt = date_du_jour.strftime("%H:%M:%S %d/%m/%Y")
	return render(request,'cle/index.html', {'date_jour':date_du_jour_txt})

def affiche_contact(request):
	if request.method=='POST':
		send_mail(request.POST['Nomdefamille'] + " " + request.POST['Prenom'] + ' [Mustélidés]', # Objet mail
		request.POST['textarea'] + "\n\nenvoyé par : " + request.POST['Mail'], # Contenu mail
		'adressemustilidae@gmail.com', # Destinataire mail
		['adressemustilidae@gmail.com'], # Destinataire
		fail_silently=False)

	return render(request, 'cle/page_contact.html', {})

def affiche_liste(request):
	return render(request, 'cle/page_liste.html', {})

def affiche_ajouter(request):
	return render(request, 'cle/page_ajouter.html', {})

def affiche_specialiste(request):
	return render(request, 'cle/page_specialiste.html', {})

def affiche_amerique(request):
	return render(request, 'cle/page_amerique.html', {})

def affiche_europe(request):
	liste_caractere=Caractere.objects.all()
	return render (request, 'cle/page_europe.html', {'liste_caractere': liste_caractere})

def caractere(request, id_caractere):
	if Caractere.objects.filter(id=id_caractere).exists():
		caractere=Caractere.objects.get(id=id_caractere)
		etat=Etat_caracteres.objects.filter(caractere=id_caractere)
	else:
		return render(request, 'cle/page_erreur.html', {'id':id_caractere})

	return render(request, 'cle/caractere.html', {'ca':caractere,'l_etat':etat})

def cle_en_cours(request, id_etat):
	caractere_test = Etat_caracteres.objects.get(id=id_etat)
	liste_espece_cara = Espece_caractere.objects.all()
	esp_possible = Espece_caractere.objects.filter(etat=caractere_test.etat) #Recupère toutes les espèces qui présentent l'état de caractère choisi.
	cara_restant = Espece_caractere.objects.exclude(caractere=caractere_test.caractere) #exclue le caractère venant d'être évalué


	etat_restant = [] #Variable pour récupérer tous les état de caractères encore à évaluer.
	nb = 0
	etat_cara_restant = [] #Même que etat_restant mais exclue en plus l'etat de caractere qui vient d'etre validé
	Liste_cara_restant = []

	for esp in esp_possible : #compte le nombre d'espèces restantes
		nb += 1
	
	if nb == 1:

		espece = esp_possible[0]
		eid = espece.espece
		print(espece)
		caid = 1
		return redirect('affiche_espece', id_espece=espece.espece.id )

	else:
		for esp in liste_espece_cara : # fonction pour récupérer tous les état de caractères encore à évaluer.
			if esp_possible.filter(espece=esp.espece).exists():
				etat_restant.append(esp)
	
		for esp in etat_restant :
			if cara_restant.filter(caractere=esp.caractere).exists():
				etat_cara_restant.append(esp)
				Liste_cara_restant.append(esp.caractere)
	
		compte_cara = Counter(Liste_cara_restant)
	
		i = -1 #compteur pour retrouver le nom du caractère dans la liste
		for cpte in compte_cara.values(): #Verifie quel caractère apparaît pour toutes les espèces encore présentes > pour trouver le caractère suivant.
			i += 1
			if cpte == nb:
				print("yay")
				value = cpte
				break
	
		liste_caracteres = []
		for cpte in compte_cara.keys():
			liste_caracteres.append(cpte)

		while i < 100 :
			nm_cara = liste_caracteres[i]
			cara_suiv = Caractere.objects.filter(nom=nm_cara)
	
			cara = cara_suiv[0] #objet caractère
			cara_pres = Espece_caractere.objects.filter(caractere=cara.id)#Recupère toutes les apparition de ce caractère dans la table complete des Etat par Especes.
			liste_apparition = []
			for esp in cara_pres:
				liste_apparition.append(esp.caractere)
	
			compte_ap = Counter(liste_apparition)
			for cpte in compte_ap.values():
				value_ap = cpte
	
			if value_ap > value:
				i += 1
				print(value_ap)
				print(value)
			else:
				break
	
	
		caid = cara.id #id du prochain caractère à évaluer.

	
	#print(cara)
	#print(caid)
	#print(compte_cara)
	#print(i)
	#print(liste_caracteres[i])
	#print(nb)
	
	return render(request, 'cle/cle_en_cours.html', {'l_esp':esp_possible,'c_test':caractere_test,'caid':caid})

def espece (request, id_espece):
    if Espece.objects.filter(id=id_espece).exists():
        espece=Espece.objects.get(id=id_espece)
    else:
        return render(request, 'cle/page_erreur.html', {'id':id_espece})

    return render(request, 'cle/espece.html', {'es':espece})