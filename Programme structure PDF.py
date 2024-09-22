# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 09:20:49 2024

@author: Silver
"""

#Partie propre à l'élève
nom = "Lois Du Hamlel Foujareau De dedinvillier"
Id = "910105"
"""
for i in range(len(data_student)):
    nom = data_student[i][0]
    Id = data_student[i][2]
"""
#Partie Structure
from fpdf import FPDF
import webbrowser
import os
import numpy as np

# Path pour l'enregistrement/la récupération des fonts
os.chdir(r'C:/Users/Silver/Desktop/PJT FORUM AM/Tentatives')

# Dimensions des pages
largeur = 210
longueur_rectangle_entete = 32.3
pages_avant = 13
    
class PG:
    #Classe PG qui prend en entrée la liste classée des secteurs préféré (en numéro)
    def __init__(self,pref):
        self.pref = pref
    
    #Programme qui permet la séléction aléatoire et le shuffle des etp recommandées
    def affectation(self):
        self.tab = []
        places = [4,2,2,2,2,2,2,2,2,2]
        for i in range(len(self.pref)):
            secteur = Secteurs[self.pref[i]-1]
            n = len(secteur)
            if(n < places[i]):
                places[i+1] += places[i]-n
                places[i] = n
            poids = [subtable[1] for subtable in secteur]
            index = []
            for k in range(n): index.append(k)
            rand = np.random.choice(index, places[i], replace=False, p=poids)
            for j in range(places[i]):
                if(len(self.tab)<7):
                    self.tab.append(secteur[rand[j]])
        np.random.shuffle(self.tab)

class PDF(FPDF):
    #Création de l'entête du PDF
    def header(self):
        self.set_margins(0,0,0)
    
        #Définition de la couleur pour les remplissages
        self.set_fill_color(142,40,98)
        #Création d'un réctangle rempli, de largeur page
        self.rect(0,0,largeur,longueur_rectangle_entete,"F")
        # Police Arial gras 15
        self.set_font('Aharoni', '', 24)
        # Titre
        self.set_fill_color(243,146,0)
        self.set_x(0)
        self.set_y(14.3)
        self.set_text_color(255,255,255)
        self.cell(109.3,18, 'Votre Parcours Forum AM', new_x="RIGHT", new_y="TOP", align='C', fill=True)
        
        self.set_xy(135,0.7)
        self.set_font('Aptos', '', 11)
        string = nom +' | Id n° : ' + Id + ' Page %s' % (self.page_no()+pages_avant)
        
        #Prise en compte de la taille du nom et de l'ID
        if (self.get_string_width(string) + 135 < largeur):
            self.cell(73.6,7.3,string,new_x="RIGHT", new_y="TOP", align='C', fill=False)
        else :
            self.cell(73.6+largeur-(self.get_string_width(string) + 135) ,7.3,string,new_x="RIGHT", new_y="TOP", align='C', fill=False)
            
        self.set_x(12.2)
        self.set_y(0.7)
        self.set_font('Aptos', '', 11)
        self.cell(91.6,7.3, 'Test d’Orientation Professionnelle pour Ingénieurs', new_x="RIGHT", new_y="TOP", align='C', fill= False)
        
        
        self.set_x(0)
        self.set_y(41.6)
        self.image("logo_forum_am.png",0,41.6,largeur,longueur_image)
        
        # Saut de ligne
        self.ln(20)
        
    #Tentative de création d'une fonction qui permet d'écrire avec gras et liens
    def mixed_text(self,text,w,l,site,police,siz):
        #rapport_police_milli = 0.375
        Symbole_gras = "<g>"
        Symbole_lien = "<l>"
        nb_c = len(text)
        indice_lettre = 0
        debut = 0
        while nb_c-3 >indice_lettre+debut:
            
            if text[debut+indice_lettre:debut+indice_lettre+3]==Symbole_gras :
                debut+=3
                lengh = 0
                gras = True
                while gras and nb_c-3 >debut+indice_lettre+lengh:
                    lengh+=1
                    if text[debut + indice_lettre+lengh:debut +indice_lettre+lengh+3]==Symbole_gras :
                        gras = False
                self.cell(self.get_string_width(text[debut:debut+indice_lettre-3]),l,text[debut:debut+indice_lettre-3], new_x="RIGHT", new_y="TOP", align='C', fill= False)
                pdf.set_font(police, "B", size = siz)
                self.cell(self.get_string_width(text[debut+indice_lettre:debut+indice_lettre+lengh]),l,text[debut+indice_lettre:debut+indice_lettre+lengh], new_x="RIGHT", new_y="TOP", align='C', fill= False)
                pdf.set_font(police, "", size = siz)
                debut = debut+indice_lettre+lengh+3
                indice_lettre =0  
                
            elif text[debut+indice_lettre:debut+indice_lettre+3]==Symbole_lien:
                indice_lettre+=3
                lengh = 0
                lien = True
                while lien and nb_c-3 >debut+indice_lettre+lengh:
                    lengh+=1
                    if text[indice_lettre+lengh:indice_lettre+lengh+3]==Symbole_gras :
                        lien = False
                self.cell(self.get_string_width(text[debut:debut+indice_lettre]),l,text[debut:debut+indice_lettre], new_x="RIGHT", new_y="TOP", align='C', fill= False)
                pdf.set_text_color(0,0,255)
                self.cell(self.get_string_width(text[debut+indice_lettre:debut+indice_lettre+lengh]),l,text[debut+indice_lettre:debut+indice_lettre+lengh], new_x="RIGHT", new_y="TOP",link = site, align='C', fill= False)
                pdf.set_text_color(0,0,0)
                debut = debut+indice_lettre+lengh
                indice_lettre =0  
                
            indice_lettre +=1 
            
        self.cell(self.get_string_width(text[debut:]),l,text[debut:], new_x="RIGHT", new_y="TOP", align='C', fill= False)
            
        
    #Fonction de classe qui permet de créer un tableau dans le format attendu, avec en indication les différentes listes liées à l'entreprise
    def tableau(self,xo,yo,Liste_etp,Liste_logo,liste_description):
        titre = [" ","Logo","Entreprise","Description/Secteur"]
        Tabl = [titre]
        for a in range(7):
            Tabl.append([" "," ",Liste_etp[a]," "])
        largeur = 186.9
        hauteur = 14.9
        column_dim = [16.2,25.8,22.8,largeur-16.2-25.8-22.8]
        dim_image = 17.5
        x = xo
        y = yo       
        x_l = xo
        y_l = yo
        x_desc = xo
        y_desc = yo
        self.set_xy(x,y)
        for i in range(8):
        #On a 7 ligne et l'entete
            for j in range(4):
            #on a 4 colonnes
                if i == 0:
                    self.set_font("aptos","B",size = 12)
                    
                elif j == 0:
                    self.set_font("aptos","B",size = 12)
                    self.set_text_color(142,40,98)
                    self.image("Point_localisation.png",xo-0.7,yo+13.4+(i-1)*hauteur,dim_image,dim_image)
                    
                    x_l,y_l = self.get_x(),self.get_y()
                    self.set_xy(xo+5.9,yo+16.2+(i-1)*hauteur)
                    #dimensions choisi avec le ppt
                    self.cell(4.44,7.6,str(i),align= "C")
                    self.set_xy(x_l,y_l)
                    
                elif j == 1:
                    self.image(Liste_logo[i-1][0],21+11.2-(Liste_logo[i-1][1]-17.5)/2,yo+(i)*hauteur,Liste_logo[i-1][1],Liste_logo[i-1][2])
                    
                elif j == 2:
                    self.set_font("aptos","B",size = 12)
                    self.set_text_color(0,0,0)

                else :
                    self.set_font("aptos","",size = 8)
                    self.set_text_color(0,0,0)
                    x_desc,y_desc = self.get_x(),self.get_y()
                    self.set_xy(x_desc+1,y_desc+1)
                    self.multi_cell(column_dim[-1]-2,4, liste_description[i-1],align= "L")
                    self.set_xy(x_desc,y_desc)
                    
                self.cell(column_dim[j],hauteur,Tabl[i][j],border = 1,new_x="RIGHT", new_y="TOP", align= "C")
            y += hauteur
            self.set_y(y)
            self.set_x(x)

    #Fonction pour souligner du texte       
    def underline_text(self, x, y,a,b, text,l):
        #a et b correspondent à la position absolue du début du texte à souligner, x y sont les positions par rapport au curseur
        self.cell(x, y, text, link=l)
        self.line(a+1, b + self.font_size, a + self.get_string_width(text)+1, b + self.font_size)
        
        
#POUR LE TEST, description génériques
desc_1="Luxe nul AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
desc_2 = "BTP nul"
desc_3 = "JSP"

#dans les tuples on a : nom fichier, dimension x, dimension y
Liste_lo=[("LVMH_logo.png",24,14.9),("Logo_1.png",14.9,14.9),("Logo_2.png",14.9,14.9),("Logo_3.png",14.9,14.9),("Logo_4.png",14.9,14.9),("Logo_5.png",14.9,14.9),("Logo_6.png",14.9,14.9)]

#Liste des secteurs/etp avec nom_etp, poids dans le secteur, position sur carte, tuple lié au logo, description
Secteurs = [[("Limagrin",0.5,[1,7],("LVMH_logo.png",24,14.9),desc_1), ("Monsanto",0.2,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Invivo",0.3,[4,2],("Logo_3.png",14.9,14.9),desc_3)], #
            [("Total",0.2,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("Shell",0.5,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Perenco",0.3,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("Danone",0.05,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("Lactalis",0.05,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Nestlé",0.9,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("Air Liquide",0.5,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("l'Oréal",0.1,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Arkema",0.4,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("Sanofi",0.25,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("Servier",0.25,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Pfizer",0.5,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("Plastic Omnium",0.2,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("Plastivaloire",0.1,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Michelin",0.7,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("Saint Gobain",0.6,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("Arcelor Mittal",0.2,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Vallourec",0.2,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("Thales",0.15,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("STMicroelectronics",0.15,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Essilor",0.7,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("LVMH",0.3,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("Hermès",0.4,[4,2],("Logo_1.png",14.9,14.9),desc_2),  ("Cartier",0.3,[4,2],("Logo_3.png",14.9,14.9),desc_3)],
            [("Schneider",0.3,[4,2],("LVMH_logo.png",24,14.9),desc_1), ("Nexans",0.3,[4,2],("Logo_1.png",14.9,14.9),desc_2), ("Legrand",0.4,[4,2],("Logo_3.png",14.9,14.9),desc_3)]]
            
#Attribution des ETP pour le PG:
Student = PG([5,3,4,2,8,6,9,1,0])
Student.affectation()
Liste_e = [i[0] for i in Student.tab]
Liste_desc = [i[4] for i in Student.tab]
Liste_lo = [i[3] for i in Student.tab]

# Création d'une instance de la classe PDF
pdf = PDF()

#Implémentation des polices nécessaires
pdf.add_font("Aharoni","","ahronbd.ttf")
pdf.add_font("Aptos","","fonnts.com-aptos.ttf")
pdf.add_font("Aptos","B","fonnts.com-aptos-black.ttf")

#Longueur de l'image AM
longueur_image = 86.5


# Ajout d'une page
pdf.add_page()

# Définir la police
pdf.set_font("aptos", size=14)


#texte de bienvenue séparé en plusieur pour les mots en gras
texte = " correspondant le mieux avec votre profil d’ingénieur pour vous permettre de vous orienter lors du jour J.\n \n Vous pouvez utiliser les résultats de ce test pour vous préparer au mieux pour votre venue au Forum. Pour plus d’informations sur les entreprises nous vous donnons rendez-vous sur notre application forum AM (disponible sur Play Store et App Store) ainsi que sur notre site web " 
texte2 = "\n \n Au plaisir de vous voir préparés le 20 novembre au Parc Floral.\n \n Cordialement, \n \n L’équipe Forum AM et TOPI"

#Rédaction et positionnement des différents élément du texte
pdf.set_xy(7.2,41.6)
pdf.set_margins(7.2,0,largeur-7.2-195.7)
pdf.write(6.21,"Le TOPI s’associe au Forum Arts et Métiers pour vous proposer un parcours d’entreprises \n")
#Partie en Gras
pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", "B", size = 14)
pdf.write(6.21,"correspondant le mieux avec votre profil d’ingénieur")

pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", size = 14)
pdf.write(6.21,texte)

pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", size = 14)
pdf.set_text_color(0,0,255)
pdf.underline_text(0,6.21,pdf.get_x(),pdf.get_y(),"forum-am.fr",'http://forum-am.fr')

pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", size = 14)
pdf.set_text_color(0,0,0)
pdf.write(6.21,texte2)

pdf.add_page()

pdf.tableau(12.2,35.4,Liste_e,Liste_lo,Liste_desc)

pdf.add_page()

#Rédaction et positionnement des différents élément du texte
pdf.set_xy(7.2,41.6)
pdf.set_font("aptos", size = 14)
pdf.set_text_color(0,0,0)
pdf.set_margins(7.2,0,largeur-7.2-195.7)
pdf.write(6.21,"Le TOPI s’associe au Forum Arts et Métiers pour vous proposer un parcours d’entreprises \n")

pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", "B", size = 14)
pdf.write(6.21,"correspondant le mieux avec votre profil d’ingénieur")

pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", size = 14)
pdf.write(6.21,texte)

pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", size = 14)
pdf.set_text_color(0,0,255)
pdf.underline_text(0,6.21,pdf.get_x(),pdf.get_y(),"forum-am.fr",'http://forum-am.fr')

pdf.set_xy(pdf.get_x(),pdf.get_y())
pdf.set_font("aptos", size = 14)
pdf.set_text_color(0,0,0)
pdf.write(6.21,texte2)
pdf.tableau(11.9,143.2,Liste_e,Liste_lo,Liste_desc)

"""
pdf.add_page()
pdf.set_font("aptos", size = 14)
pdf.mixed_text("test test <g>test<g> test test <g> test test <g> test test",10,10,site = None,police = "aptos",siz = 14)
"""
# Enregistrement du PDF
pdf_output_path = "Structure PDF.pdf"
pdf.output(pdf_output_path)

# Vérification si le fichier a été enregistré avec succès
if os.path.exists(pdf_output_path):
    # Ouvrir le fichier PDF dans Mozilla Firefox
    webbrowser.open_new_tab(f'file://{os.path.realpath(pdf_output_path)}')
else:
    print("Erreur lors de la création du PDF")
