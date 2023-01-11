#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: pays
#------------------------------------------------------------

CREATE TABLE pays(
        code_pays Char (2) NOT NULL ,
        nom_pays  TinyText NOT NULL ,
        continent TinyText ,
        code_iso3 Char (3)
	,CONSTRAINT pays_PK PRIMARY KEY (code_pays)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: zone-économique
#------------------------------------------------------------

CREATE TABLE zone_economique(
        id_ze   Int NOT NULL ,
        code_ze Varchar (20) NOT NULL ,
        nom_ze  TinyText NOT NULL
	,CONSTRAINT zone_economique_PK PRIMARY KEY (id_ze)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: sections
#------------------------------------------------------------

CREATE TABLE sections(
        code_section    Int NOT NULL ,
        nom_section     Varchar (32) NOT NULL ,
        libelle_section TinyText NOT NULL ,
        libelle_short   Varchar (50) NOT NULL
	,CONSTRAINT sections_PK PRIMARY KEY (code_section)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: sous_sections
#------------------------------------------------------------

CREATE TABLE sous_sections(
        code_ss_section    Char (4) NOT NULL ,
        libelle_ss_section Mediumtext NOT NULL
	,CONSTRAINT sous_sections_PK PRIMARY KEY (code_ss_section)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: produit
#------------------------------------------------------------

CREATE TABLE produit(
        code_NC8        Char (8) NOT NULL ,
        libelle_NC8     Text NOT NULL ,
        code_usup       Int NOT NULL ,
        nom_usup        Text ,
        code_ss_section Char (4) ,
        code_section    Int
	,CONSTRAINT produit_PK PRIMARY KEY (code_NC8)

	,CONSTRAINT produit_sous_sections_FK FOREIGN KEY (code_ss_section) REFERENCES sous_sections(code_ss_section)
	,CONSTRAINT produit_sections0_FK FOREIGN KEY (code_section) REFERENCES sections(code_section)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: transaction
#------------------------------------------------------------

CREATE TABLE transaction(
        id_transaction Int NOT NULL ,
        flux           Char (1) NOT NULL ,
        mois           Int NOT NULL ,
        annee          Int NOT NULL ,
        valeur         Float NOT NULL ,
        Masse          Float NOT NULL ,
        code_NC8       Char (8) NOT NULL ,
        code_pays      Char (2) NOT NULL
	,CONSTRAINT transaction_PK PRIMARY KEY (id_transaction)

	,CONSTRAINT transaction_produit_FK FOREIGN KEY (code_NC8) REFERENCES produit(code_NC8)
	,CONSTRAINT transaction_pays0_FK FOREIGN KEY (code_pays) REFERENCES pays(code_pays)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: ze_pays
#------------------------------------------------------------

CREATE TABLE ze_pays(
        id_ze     Int NOT NULL ,
        code_pays Char (2) NOT NULL
	,CONSTRAINT ze_pays_PK PRIMARY KEY (id_ze,code_pays)

	,CONSTRAINT ze_pays_zone_economique_FK FOREIGN KEY (id_ze) REFERENCES zone_economique(id_ze)
	,CONSTRAINT ze_pays_pays0_FK FOREIGN KEY (code_pays) REFERENCES pays(code_pays)
)ENGINE=InnoDB;

