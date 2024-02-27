import  mysql.connector
from datetime import datetime

from mysql.connector import  Error

def connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='informatique'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"erreur{e}")
        return None


def crud():
    print("Bienvenue dans le Menu d'action")
    print("[1] Créer un langage")
    print("[2] Supprimer un langage")
    print("[3] Modifier un langage")
    print("[4] liste de tous les langages")
    print("[5] afficher un langage")
    print("[6] afficher les logs")
    print("[7] quitter le programme")
    return input("Faites votre choix")

def create_langage(nom, date, level):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO languages (nom,date_creation,level) VALUES (%s,%s,%s)"
            cursor.execute(query, (nom,date,level))
            conn.commit()
            print(f"User '{nom} added successfully")
        except Error as e:
            print((f"Erreur lors de l'ajout de l'utilisateur: {e}"))
        finally:
            cursor.close()
            conn.close()

def delete_langage(language_id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM languages WHERE id = %s"
            cursor.execute(query, (language_id,))
            conn.commit()
            print(f"User ID'{language_id} has been deleted")
        except Error as e:
            print((f"Erreur lors de la suppresion de l'utilisateur: {e}"))
        finally:
            cursor.close()
            conn.close()

def update_langage(language_id,name,date_creation,level):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            if name != None and date_creation != None and level != None:
                query = "UPDATE languages SET nom = %s, date_creation = %s, level = %s WHERE id = %s"
                cursor.execute(query, (name, date_creation,level,language_id,))
                conn.commit()
                print(f"User ID'{language_id} has been updated to '{name}'.")
            elif name != None and date_creation != None and level == None:
                query = "UPDATE languages SET nom = %s, date_creation = %s WHERE id = %s"
                cursor.execute(query, (name, date_creation,language_id,))
                conn.commit()
                print(f"User ID'{language_id} has been updated to '{name}'.")
            elif name != None and date_creation == None and level == None:
                query = "UPDATE languages SET nom = %s WHERE id = %s"
                cursor.execute(query, (name, language_id,))
                conn.commit()
                print(f"User ID'{language_id} has been updated to '{name}'.")
        except Error as e:
            print((f"Erreur lors de la mise à jour de l'utilisateur: {e}"))
        finally:
            cursor.close()
            conn.close()

def one_language(language_id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "SELECT nom, date_creation, level FROM languages WHERE id = %s"
            cursor.execute(query, (language_id,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    language_name, creation_date, level = row
                    print("Nom:", language_name)
                    print("Date de création:", creation_date)
                    print("Level:", level)
            else:
                print("Langage non trouvé.")
            conn.commit()
        except Error as e:
            print((f"Erreur lors de la lecture des langages: {e}"))
        finally:
            conn.close()
def all_languages():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nom,date_creation FROM languages")
            return cursor.fetchall()
        except Error as e:
            print(f"Erreur lors de la lecture des utilisateurs: {e}")
            return None
        finally:
            conn.close()

def Message_Historique(nom):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO log (message) VALUES (%s)"
            cursor.execute(query, (nom,))
            conn.commit()
        except Error as e:
            print((f"Erreur lors de l'ajout de l'utilisateur: {e}"))
        finally:
            cursor.close()
            conn.close()

def verification_name_user(name_user):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            if name_user != None:
                query = "SELECT nom FROM users WHERE nom = %s"
                cursor.execute(query, (name_user,))
                resultats = cursor.fetchall()
                if resultats:
                    print(f"'{name_user}' vous êtes connecté.")
                else:
                    print(f"'{name_user}' n'a pas été trouvé dans la base de données.")
                    exit()
                conn.commit()
        except Error as e:
            print((f"Erreur lors de la vérification de l'utilisateur: {e}"))
        finally:
            cursor.close()
            conn.close()

def All_Logs():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Message FROM log")
            return cursor.fetchall()
        except Error as e:
            print(f"Erreur lors de la lecture des utilisateurs: {e}")
            return None
        finally:
            conn.close()

programme = True

while(programme):
    name_user = input("Quel est votre nom d'utilsateur ?")
    verification_name_user(name_user)
    choice = crud()
    print(choice)
    choice = int(choice)
    if choice == 1:
        nom = input("Quel est le nom du langage que vous voulez créer ?")

        date = input("Quel est la date du langage que vous voulez créer ?")

        level = input("Quel est le level du langage que vous voulez créer ?")

        langage = create_langage(nom, date, level)

        Message_Historique(f"L'user {name_user} a ajouté {nom}, le  {str(datetime.now())}")

    elif choice == 2:
        language_id = input("Quel est le langage que vous voulez supprimer ?")

        langage  = delete_langage(language_id)

        Message_Historique(f"L'user {name_user} a supprimé l'id {language_id}, le {str(datetime.now())}")

    elif choice == 3:
        language_id = input("Quel est le numéro du langage qui doit être modifié?")

        name = input("Quel est le nouveau nom de ce langage?")

        date_creation = input("Quel est la nouvelle date de ce langage?")

        level = input("Quel est le nouveau level de ce langage ?")

        langage = update_langage(language_id,name,date_creation,level)

        Message_Historique(f"L'user {name_user} a modifié {name}, le {str(datetime.now())}")

    elif choice == 4:

        langages = all_languages()

        if langages is not None:
            for (nom, date_creation) in langages:
                print(f"Nom : {nom} , Date de création: {str(datetime.now())}")
        else:
            print("Aucune donnée disponible.")

    elif choice == 5:
        language_id = input("Quel est le numéro du langage que vous voulez affiché ?")

        one_language(language_id)
    elif choice == 6:
        logs = All_Logs()
        if logs is not None:
            for logs in logs:
                print(f"Message : {logs}")
        else:
            print("Les Logs sont vides")
    elif choice == 7:
        programme = False
    else:
        pass