import cv2
import pytesseract
import fitz  # PyMuPDF
import pdfplumber
import re
from collections import namedtuple
import pandas as pd
import streamlit as st 
from request import *
import os 
import pandas as pd
import json

chemin_tesseract=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd=chemin_tesseract

import uuid
st.title("Extraction des Données")
logo_path = "gproconsulting.png" 
st.sidebar.image(logo_path, use_column_width=True)
type_facture = st.sidebar.selectbox("Sélectionner le type de facture", ["DESIPRO PTE LTD", "Société Sublitunis", "DECOTHLON PRODU ZIONE ITALIA", "VTL", "CARVICO"])

def choisir_fichier():
    fichier = st.file_uploader("Choisissez un fichier", type=["jpg", "jpeg", "png", "pdf"])
    chemin_fichier = None  # Initialisation de la variable
    if fichier is not None:
        os.makedirs('temp', exist_ok=True)
        chemin_fichier = os.path.join('temp', fichier.name)
        with open(chemin_fichier, 'wb') as f:
            f.write(fichier.getbuffer())
    return chemin_fichier

def extraire_informations_document(chemin_fichier):
    informations_extraites = None  
    if chemin_fichier is not None:
        if chemin_fichier.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Traitement pour les fichiers image
            informations_extraites = extraire_informations_image(chemin_fichier)     
        elif chemin_fichier.lower().endswith('.pdf'):
            
            informations_extraites = extraire_informations_pdf(chemin_fichier)
        else:
            st.error("Format de fichier non pris en charge")
    else:
        st.warning("Aucun fichier sélectionné")
    return informations_extraites 


def extraire_informations_image(chemin_image):
    image = cv2.imread(chemin_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    texte_brut = ""
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            roi = image[y:y+h, x:x+w]
            texte_extrait = pytesseract.image_to_string(roi, lang='eng')
            texte_brut += texte_extrait 
    informations = {"texte": texte_brut}
    return informations


def extraire_informations_pdf(chemin_pdf):
    texte_extrait = None  
    try:
        with pdfplumber.open(chemin_pdf) as pdf:
            page = pdf.pages[0]
            texte_extrait = page.extract_text()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Le fichier PDF '{chemin_pdf}' n'a pas été trouvé.") from e
    except Exception as e:
        raise Exception(f"Une erreur est survenue lors de l'extraction des informations du PDF '{chemin_pdf}'.") from e
    informations_extraites = {
        "texte": texte_extrait,
    }
    return informations_extraites


def traitement_Sublitunis_pdf(informations):
    informations_extraites =informations["texte"]
    nom_pattern = r"^(.*?)\n"
    pieces_pattern=r"\b\d+ R\d+\b"
    metrage_pattern=r"\b\d+\s(?=\d{2}/\d{2}/\d{4})"
    date_pattern = r"Date : (\d{2}-\d{2}-\d{4})"
    date_pro_pattern = r"\b\d+\s(\d{2}/\d{2}/\d{4})\b"
    num_commande_pattern = r"N°commande : (\d+)"
    destinataire_pattern = r"Destinataire : (\w+)"
    nb_rouleaux_pattern = r"Nombre de rlx (\d+)"
    # Extraction des informations avec les expressions régulières
    nom_match = re.search(nom_pattern, informations_extraites)
    date_match = re.search(date_pattern, informations_extraites)
    num_commande_match = re.search(num_commande_pattern, informations_extraites)
    destinataire_match = re.search(destinataire_pattern, informations_extraites)
    nb_rouleaux_match = re.search(nb_rouleaux_pattern, informations_extraites)
    pieces_match= re.findall(pieces_pattern, informations_extraites)
    date_pro_match=re.findall(date_pro_pattern , informations_extraites)
    metrage_match=re.findall(metrage_pattern,informations_extraites)
    if nom_match:
        nom = nom_match.group(1)
    else:
        nom = "Nom non trouvé"
    if date_match:
        date = date_match.group(1)
    else:
        date = "Date non trouvée"
    if num_commande_match:
        num_commande = num_commande_match.group(1)
    else:
        num_commande = "Numéro de commande non trouvé"
    if destinataire_match:
        destinataire = destinataire_match.group(1)
    else:
        destinataire = "Destinataire non trouvé"
    if nb_rouleaux_match:
        nb_rouleaux = nb_rouleaux_match.group(1)
    else:
        nb_rouleaux = "Nombre de rouleaux non trouvé"
    if pieces_match:
        n_pieces= pieces_match
    else:
         n_pieces="numero pieces non trouvé"
    if date_pro_match:
        date_pro=date_pro_match
    else:
        date_pro="date prod non trouvé"
    if metrage_match:
        metrage=metrage_match
    else:
        metrage="metrage non trouvé"

    # Affichage des résultats
    st.write("Nom:", nom)
    st.write("Date:", date)
    st.write("Numéro de commande:", num_commande)
    st.write("Destinataire:", destinataire)
    st.write("Nombre de rouleaux:", nb_rouleaux)
    st.write("Numero pieces")
    for resultat ,date_pro ,metrage in zip(n_pieces,date_pro,metrage):
        st.write(resultat)
        st.write(date_pro)
        st.write(metrage)


def traitement(chemin_fichier, type_facture, informations_extraites):
    if chemin_fichier.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        if type_facture == "Société Sublitunis":
            traitement_Sublitunis_image(informations_extraites)
        elif type_facture == "DESIPRO PTE LTD":
            st.info("La fonction DESIPRO n'est pas implémentée pour les images")  
        elif type_facture == "DECOTHLON PRODU ZIONE ITALIA":
            st.info("La fonction DECOTHLON n'est pas implémentée pour les images")
        elif type_facture == "VTL":
            st.info("La fonction VTL n'est pas implémentée pour les images")
        elif type_facture == "CARVICO":
            st.info("La fonction CARVICO n'est pas implémentée pour les images")
        else:
            st.error("Type de facture non pris en charge pour les images")
    elif chemin_fichier.lower().endswith('.pdf'):
        if type_facture == "Société Sublitunis":
            traitement_Sublitunis_pdf(informations_extraites)
        elif type_facture == "DESIPRO PTE LTD":
            st.info("La fonction DESIPRO n'est pas implémentée pour les PDF")  
        elif type_facture == "DECOTHLON PRODU ZIONE ITALIA":
            st.info("La fonction DECOTHLON n'est pas implémentée pour les PDF")
        elif type_facture == "VTL":
            st.info("La fonction VTL n'est pas implémentée pour les PDF")
        elif type_facture == "CARVICO":
            st.info("La fonction CARVICO n'est pas implémentée pour les PDF")
        else:
            st.error("Type de facture non pris en charge pour les PDF")
    else:
        st.error("Format de fichier non pris en charge")

def traitement_Sublitunis_image(informations):
        informations_extraites =informations["texte"]
        nom_pattern = r"Destinataire\s+:\s+Enfavet\s+([\s\S]*?)\s+LISTE\s+DE\s+COLISAGE"
        pieces_pattern=r"\b\d+ R\d+\b"
        metrage_pattern=r"\d{2}/\d{2}/\d{4}\s+(\d{2,})"
        date_pattern = r"Date :\s*(\d{2}-\d{2}-\d{4})"
        date_pro_pattern = r"\b\d{2}/\d{2}/\d{4}\b"
        num_commande_pattern = r"N°commande : (\d+)"
        destinataire_pattern = r"Destinataire : (\w+)"
    # Extraction des informations avec les expressions régulières
        nom_match = re.search(nom_pattern, informations_extraites)
        date_match = re.search(date_pattern, informations_extraites)
        num_commande_match = re.search(num_commande_pattern, informations_extraites)
        destinataire_match = re.search(destinataire_pattern, informations_extraites)
        pieces_match= re.findall(pieces_pattern, informations_extraites)
        date_pro_match=re.findall(date_pro_pattern , informations_extraites)
        metrage_match=re.findall(metrage_pattern,informations_extraites)
        if nom_match:
            nom = nom_match.group(1)
        else:
            nom = "Nom de la société  non trouvé"
            alerte(nom) 
        if date_match:
            date = date_match.group(1)
        else:
            date = "Date non trouvée"
            alerte(date)
        if num_commande_match:
            num_commande = num_commande_match.group(1)
        else:
            num_commande = "Numéro de commande non trouvé"
            alerte(num_commande)
        if destinataire_match:
            destinataire = destinataire_match.group(1)
        else:
                destinataire = "Destinataire non trouvé"
                alerte(destinataire)
        if pieces_match:
            n_pieces= pieces_match
        else:
            n_pieces="numero pieces non trouvé"
            alerte(n_pieces)
        if date_pro_match:
            date_pro=date_pro_match
        else:
            date_pro="date prod non trouvé"
            alerte(date_pro)
        if metrage_match:
            metrage=metrage_match
        else:
            metrage="metrage non trouvé"
            alerte(metrage)

        # Affichage des résultats
        st.write("Nom:", nom)
        st.write("Date:", date)
        st.write("Numéro de commande:", num_commande)
        st.write("Destinataire:", destinataire)
        st.write("Numero pieces")
        for resultat ,date_pro ,metrage in zip(n_pieces,date_pro,metrage):
            st.write(resultat)
            st.write(date_pro)
            st.write(metrage)


def alerte(message):
    st.markdown(f'<div style="background-color:#ffcccc;padding:10px;border-radius:5px;"><p style="color:red;">{message}</p></div>', unsafe_allow_html=True)


chemin_fichier = choisir_fichier()
if chemin_fichier:
    informations_extraites = extraire_informations_document(chemin_fichier)
    st.write("Informations extraites :", informations_extraites)
    if informations_extraites:
        traitement(chemin_fichier,type_facture, informations_extraites)
    else:
        print("Aucune information extraite du fichier PDF.")
else:
    print("Aucun fichier PDF sélectionné.")
