from django.shortcuts import render,redirect
from datetime import datetime
from collections import Counter
from django.core.mail import send_mail
import smtplib
from cle.models import Espece, Caractere, Etat_caracteres, Espece_caractere, Cle

def accueil(request):
	date_du_jour = datetime.now()
	date_du_jour_txt = date_du_jour.strftime("%H:%M:%S %d/%m/%Y")
	return render(request,'cle/index.html', {'date_jour':date_du_jour_txt})

def affiche_contact(request):

	if request.method=='POST':
		try :
			send_mail(request.POST['Nomdefamille'] + " " + request.POST['Prenom'] + ' [Mustélidés]', # Objet mail
			request.POST['textarea'] + "\n\nenvoyé par : " + request.POST['Mail'], # Contenu mail
			'adressemustilidae@gmail.com', # Destinataire mail
			['adressemustilidae@gmail.com'], # Destinataire
			fail_silently=False)
		except smtplib.SMTPDataError as e:
			print('Exception : ' + 'SMTPDataError' + ' Probablement trop de connections journalieres sur le serveur smtp')
		else :
			print('Exception inconnue')
	return render(request, 'cle/page_contact.html', {})

def affiche_liste(request):
	return render(request, 'cle/page_liste.html', {})

def affiche_ajouter(request):
	print('Hello world')
	# Espece.objects.create(nom='vache')
	# Cle.objects.create(nom='hi')
	if request.method=='POST':
		print('Request Data :' + str(request.POST))
		print('Cle Region :' + request.POST['cleRegion'])
		print('Nom espece :' + request.POST['espName'])
		
			
		print('Nom latin :' + request.POST['latinName'])
		print('Description :' + request.POST['description'])
		print('Post members :' + str(len(request.POST)))
		

		# Partie pour regarder Si la cle de region existe
		# si elle n'existe pas on la cree
		if (not Cle.objects.filter(nom=request.POST['cleRegion']).exists()):
			cleRegion = Cle.objects.create(nom=request.POST['cleRegion'])
		else :
			cleRegion = Cle.objects.filter(nom=request.POST['cleRegion'])[0]
		print('La cle de region id : ' + str(cleRegion.id))


		# On regarde si l'espece existe deja, si elle existe,
		# on ne rempli pas la base de donnees
		if (Espece.objects.filter(nom=request.POST['espName']).exists()):
			print('L\'espece est deja repertoriee')
			return render(request, 'cle/page_ajouter.html', {})
		
		# On cree une nouvelle espece dans la BD avec son nom,
		# son nom latin et sa description
		cleEspece = Espece.objects.create(nom=request.POST['espName'], \
		nom_latin=request.POST['latinName'], description=request.POST['description'], cle_name_id=cleRegion.id)


		# On etabli combien de caracteres sont presents dans le formulaire
		# en se basant sur la taille du formulaire
		# 4 champs d'input + 1 token = 5 
		# 2 champs par caractere
		caracteresRestants = (len(request.POST) - 5) / 2
		print('Remaining caracteres :' + str(caracteresRestants))
		
		i = 0
		while (caracteresRestants > 0):
			print('search ', caracteresRestants)
			while not str('caractere' + str(i)) in request.POST:
				i += 1
			print('found at :', str(i))
			print('Nom caractere ' + str(i) + ' :', request.POST['caractere' + str(i)] )
			print('etat ' + str(i) + ' :', request.POST['etat' + str(i)] )
			if (not Caractere.objects.filter(nom=request.POST['caractere' + str(i)]).exists()):
				cleCaractere = Caractere.objects.create(nom=request.POST['caractere' + str(i)])
			else :
				cleCaractere = Caractere.objects.filter(nom=request.POST['caractere' + str(i)])[0]
			
			if (not Etat_caracteres.objects.filter(etat=request.POST['etat' + str(i)]).exists()):
				cleEtat= Etat_caracteres.objects.create(etat=request.POST['etat' + str(i)], caractere_id=cleCaractere.id)
			else :
				cleEtat = Etat_caracteres.objects.filter(etat=request.POST['etat' + str(i)])[0]
			Espece_caractere.objects.create(etat=request.POST['etat' + str(i)],
														caractere_id=cleCaractere.id,
														espece_id=cleEspece.id)
			
			i += 1
			caracteresRestants -= 1
		





	# if (Espece.objects.filter(nom='vache').exists()):
	# 	Espece.objects.create(nom='cochondingue', nom_latin='dingding', description='oui', cle_name_id=1)
	# 	print()
	# else :
	# 	Espece.objects.create(nom='vache', nom_latin='vachium', description='jajajaja', cle_name_id=1)
	# 	print()
	## AJOUTER / VERIFIER NOUVELLE ESPECE
	# NOM | NOM_LATIN | DESCRIPTION | CLE_NAME_ID => Auto : NOM ID
	##


	# FOR NOMBRE DE CARRACTERES:
		## AJOUTER / VERIFIER CARACTERE
		# NOM_CARACTERE -> Auto : CARACTERE ID

		##


		## AJOUTER / VERIFIER ETAT CARACTERE
		#  ETAT | CARACTERE ID 

		##	

		## AJOUTER / VERIFIER CARACTERE ESPECE
		#  ETAT | CARACTERE ID | ESPECE ID

		##
	# END
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
