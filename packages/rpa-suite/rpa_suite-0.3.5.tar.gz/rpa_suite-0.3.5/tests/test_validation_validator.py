import unittest
from rpa_suite.validate.mail_validator import valid_emails

class TestValidEmails(unittest.TestCase):

    def test_validator_emails(self):
        # Defina alguns valores de entrada e o resultado esperado
        entrada = ['camilo.carvalho@triasoftware.com.br', 'asfaltorodas@gmail.com']
        esperado = 2

        # Chame a função com a entrada
        dictio = valid_emails(entrada)
        resultado = len(dictio['emails_validos'])
        # Verifique se o resultado é o esperado
        self.assertEqual(resultado, esperado)

if __name__ == '__main__':
    unittest.main()
