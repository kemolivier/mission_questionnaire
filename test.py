import os
import unittest
from unittest.mock import patch
import questionnaire


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
        self.assertEqual(q.categorie,"Inconnue")
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
        pass


if __name__ == '__main__':
    unittest.main()
else:
    print(__name__)
