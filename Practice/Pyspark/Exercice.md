Retail Example
==============

Databricks : https://community.cloud.databricks.com

URL du CSV : https://we.tl/t-r0HmCi0BBQ

References : 
- https://github.com/kevinschaich/pyspark-cheatsheet
- https://images.datacamp.com/image/upload/v1676302905/Marketing/Blog/PySpark_SQL_Cheat_Sheet.pdf


Informations sur le fichier de données :
=======================================

Il s'agit d'un ensemble de données transnational qui contient toutes les transactions effectuées entre le 01/12/2010 et le 09/12/2011 pour un commerce de détail en ligne non implanté physiquement, basé et enregistré au Royaume-Uni. L'entreprise vend principalement des cadeaux uniques pour toutes occasions. De nombreux clients de l'entreprise sont des grossistes.

Informations sur les attributs :
===============================

InvoiceNo : Numéro de facture. Nominal, un nombre entier de 6 chiffres attribué de manière unique à chaque transaction. Si ce code commence par la lettre 'C', cela indique une annulation.
StockCode : Code produit (article). Nominal, un nombre entier de 5 chiffres attribué de manière unique à chaque produit distinct.
Description : Nom du produit (article). Nominal.
Quantity : Quantité de chaque produit (article) par transaction. Numérique.
InvoiceDate : Date et heure de la facture. Numérique, le jour et l'heure auxquels chaque transaction a été générée.
UnitPrice : Prix unitaire. Numérique, prix du produit par unité en livres sterling.
CustomerID : Numéro de client. Nominal, un nombre entier de 5 chiffres attribué de manière unique à chaque client.
Country : Nom du pays. Nominal, le nom du pays où réside chaque client.

Questions :
===============================

1. **Filtrer et compter les annulations**
   - **Tâche** : Trouver le nombre total de transactions annulées.

2. **Top 5 des produits les plus populaires**
   - **Tâche** : Identifier les 5 produits les plus fréquemment commandés en fonction de la `Quantity`.

3. **Revenu par pays**
   - **Tâche** : Calculer le revenu total généré dans chaque pays, en excluant les transactions annulées.

4. **Tendance des ventes mensuelles**
   - **Tâche** : Calculer le revenu total des ventes pour chaque mois dans l'ensemble de données.

5. **Client avec les dépenses les plus élevées**
   - **Tâche** : Trouver le client qui a dépensé le plus sur toute la période.

6. **Identifier les modèles de vente saisonniers**
   - **Tâche** : Analyser les tendances saisonnières en calculant le revenu mensuel moyen et déterminer si certains mois présentent des écarts significatifs.

7. **Taux de clients récurrents**
   - **Tâche** : Déterminer le pourcentage de transactions effectuées par des clients récurrents.

8. **Distribution de la taille des factures**
   - **Tâche** : Calculer la taille moyenne de chaque facture en termes de `Quantity` et de `Revenue`.

9. **Identifier les paires de produits les plus fréquentes**
   - **Tâche** : Trouver les paires de produits les plus fréquemment achetées ensemble dans une même facture.

Ces exercices couvrent différents aspects de l'analyse de données en PySpark pour explorer et comprendre les ventes et le comportement des clients dans cet ensemble de données.
