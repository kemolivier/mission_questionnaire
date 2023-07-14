import os
import unittest
from unittest.mock import patch
import questionnaire
import questionnaire_import
import json


def additionner(a, b):
    return a + b


def conversion_nombre():
    num_str = input("Rentrez un nombre : ")
    return int(num_str)


class TestsUnitaireDemo(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):  # reinitialisation (remise à zero)
        print("tearDown")

    def test_toto(self):
        print("TOTO")

    def test_additionner_nombres_positifs(self):
        print("test_additionner_nombres_positifs")
        self.assertEqual(additionner(5, 10), 15)
        self.assertEqual(additionner(6, 10), 16)
        self.assertEqual(additionner(7, 10), 17)
        self.assertEqual(additionner(8, 10), 18)

    def test_additionner_nombres_negatifs(self):
        print("test_additionner_nombres_negatifs")
        self.assertEqual(additionner(-5, -10), -15)
        self.assertEqual(additionner(-6, -10), -16)
        self.assertEqual(additionner(-7, -10), -17)
        self.assertEqual(additionner(-8, -10), -18)

    def test_conversion_nombre_valide(self):
        print("test_conversion_nombre_valide")
        with patch("builtins.input", return_value="10"):
            self.assertEqual(conversion_nombre(), 10)

        with patch("builtins.input", return_value="100"):
            self.assertEqual(conversion_nombre(), 100)

    def test_conversion_entree_invalide(self):
        with patch("builtins.input", return_value="aaa"):
            self.assertRaises(ValueError, conversion_nombre)


class TestsQuestion(unittest.TestCase):
    def test_question_bonne_mauvaise_reponse(self):
        choix = ("choix1", "choix2", "choix3")
        q = questionnaire.Question("titre_question", choix, "choix2")
        with patch("builtins.input", return_value="1"):  # Comme si on avait entrez "1" au clavier
            self.assertFalse(q.poser(1, 1))
        with patch("builtins.input", return_value="2"):  # Comme si on avait entrez "2" au clavier
            self.assertTrue(q.poser(1, 1))

        with patch("builtins.input", return_value="3"):  # Comme si on avait entrez "3" au clavier
            self.assertFalse(q.poser(1, 1))


class TestsQuestionnaire(unittest.TestCase):
    def test_questionnaire_lancer_alien_debutant(self):
        filename = os.path.join("test_data", "cinema_alien_debutant.json")  # Fonctionne sur Mac et windows
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)  # Permet de s'assurer que le questionnaire qu'on a recuperé n'est pas egale à None

        # nb de questions
        self.assertEqual(len(q.questions), 10)

        # titre, categorie, difficulté
        self.assertEqual(q.titre, "Alien")
        self.assertEqual(q.categorie, "Cinéma")
        self.assertEqual(q.difficulte, "débutant")

        # patcher le input -> forcer de répondre toujours à 1 --> score c'est 4
        with patch("builtins.input",
                   return_value="4"):  # Comme si on avait entrez "4" au clavier, donc on choisit le quatriéme choix de reponse
            self.assertEqual(q.lancer(), 6)

    def test_questionnaire_format_invalide(self):
        filename = os.path.join("test_data", "format_invalide1.json")  # Fonctionne sur Mac et windows
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)  # Permet de s'assurer que le questionnaire qu'on a recuperé n'est pas egale à None
        self.assertEqual(q.categorie, "Inconnue")
        self.assertEqual(q.difficulte, "Inconnue")
        self.assertIsNotNone(q.questions)

        filename = os.path.join("test_data", "format_invalide2.json")  # Fonctionne sur Mac et windows
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNotNone(q)  # Permet de s'assurer que le questionnaire qu'on a recuperé n'est pas egale à None
        self.assertEqual(q.categorie, "Inconnue")
        self.assertEqual(q.difficulte, "Inconnue")
        self.assertIsNotNone(q.questions)

        filename = os.path.join("test_data", "format_invalide3.json")  # Fonctionne sur Mac et windows
        q = questionnaire.Questionnaire.from_json_file(filename)
        self.assertIsNone(q)


class TestsImportQuestionnaire(unittest.TestCase):
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats",
                                                "https://www.kiwime.com/oqdb/files/1050828847/OpenQuizzDB_050/openquizzdb_50.json")

        filenames = ("animaux_leschats_confirme.json", "animaux_leschats_debutant.json", "animaux_leschats_expert.json")

        for filename in filenames:
            self.assertTrue(os.path.isfile(filename))
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            try:
                data = json.loads(json_data)
            except:
                self.fail("Problème de désérialisation pour le fichier " + filename)

            self.assertIsNotNone(data.get("titre"))
            self.assertIsNotNone(data.get("questions"))
            self.assertIsNotNone(data.get("difficulte"))
            self.assertIsNotNone(data.get("categorie"))

            # on va boucler sur les questions
            for question in data.get("questions"):
                self.assertIsNotNone(question.get("titre"))
                self.assertIsNotNone(question.get("choix"))
                for choix in question.get("choix"):
                    # s'assurer que le titre du choix est superieur ou égal à "0"
                    self.assertGreater(len(choix[0]), 0)
                    # s'assurer que le choix de 1 est un booléen
                    self.assertTrue(isinstance(choix[1], bool))

                # Verifier que parmi tous ses choix, on a bien qu'une seule bonne réponse
                # On recupere les bonnes réponse sur une question
                bonne_reponses = [i[0] for i in question.get("choix") if i[1] == True]
                # On verifie qu'on a une bonne réponse
                self.assertEqual(len(bonne_reponses), 1)

            # titre, questions, difficulte, categorie
            # question -> titre, choix
            #   choix -> longueur du titre > 0
            #         -> 2ème champ est bien un bool isinstance(..., bool)
            #   -> il y a bien une seule bonne réponse


if __name__ == '__main__':
    unittest.main()
else:
    print(__name__)
