import unittest
from rpa_suite.email.sender_smtp import enviar_email
from cred.credentials import mail_pass


class TestEmail(unittest.TestCase):

    def test_send_mail(self):
        
        # Defina alguns valores de entrada e o resultado esperado
        entrada = ['camilo.carvalho@triasoftware.com.br',
                    mail_pass,
                    ['asfaltorodas@gmail.com', 'camilo.costa1993@gmail.com'],
                    'Ola Camilo teste',
                    'mensagem no corpo do email de teste ...']
        esperado = len(entrada[2])

        # Chame a função com a entrada
        dictio = enviar_email(*entrada)
        resultado = dictio['quantidade_enviada']
        
        # Verifique se o resultado é o esperado
        self.assertEqual(resultado, esperado)

if __name__ == '__main__':
    unittest.main()
