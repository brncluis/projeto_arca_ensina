# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.urls import reverse
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from datetime import date
# import time

# from usuarios.models import Usuario
# from dashboard.models import Paciente, Consulta, Conduta


# class CondutasCriticasProntuarioTests(StaticLiveServerTestCase):

#     def setUp(self):
#         chrome_options = Options()
#         chrome_options.add_argument('--window-size=1280,960')

#         service = Service(ChromeDriverManager().install())
#         self.selenium = webdriver.Chrome(
#             service=service,
#             options=chrome_options
#         )

#         self.selenium.implicitly_wait(5)

#         self.usuario = Usuario.objects.create_superuser(
#             username='medico_critico',
#             email='medico@teste.com',
#             password='admin123',
#             id_acesso='123456'
#         )

#         self.paciente = Paciente.objects.create(
#             nome_completo="João Silva",
#             data_nascimento="2000-01-01",
#             peso=70,
#             genero="M",
#             altura=175,
#             nome_mae="Maria Silva",
#             nome_pai="José Silva"
#         )

#         self.consulta = Consulta.objects.create(
#             paciente=self.paciente,
#             data_consulta=date.today(),
#             alergias="Nenhuma",
#             doencas_cronicas="Nenhuma",
#             cirurgias_anteriores="Nenhuma",
#             medicamentos_uso_continuo="Nenhum",
#             queixa_principal="Febre alta",
#             historico_de_doenca_atual="Paciente com sinais de alerta",
#             frequencia_respiratoria="20",
#             pressao_arterial="120/80",
#             frequencia_cardiaca="90",
#             temperatura="39",
#             saturacao="97",
#             ausculta_pulmonar="Normal",
#             estado_geral="Grave",
#             exames_solicitados="Hemograma",
#             diagnostico_provisorio="Suspeita de dengue"
#         )

#     def tearDown(self):
#         self.selenium.quit()

#     def login(self):
#         self.selenium.get(f'{self.live_server_url}/usuarios/login/')
#         time.sleep(1)

#         self.selenium.find_element(By.ID, 'id_acesso').clear()
#         self.selenium.find_element(By.ID, 'id_acesso').send_keys('123456')

#         self.selenium.find_element(By.ID, 'password').clear()
#         self.selenium.find_element(By.ID, 'password').send_keys('admin123')

#         self.selenium.find_element(By.CSS_SELECTOR, '[type=submit]').click()
#         time.sleep(2)

#     def abrir_prontuario(self):
#         url_prontuario = reverse(
#             'prontuario_paciente',
#             args=[self.paciente.id]
#         )

#         self.selenium.get(self.live_server_url + url_prontuario)
#         time.sleep(2)

#     def test_conduta_critica_aparece_destacada_no_prontuario(self):
#         """
#         Cenário Positivo:

#         Dado que o médico está autenticado e na aba de pacientes
#         E o prontuário possui uma conduta marcada como crítica
#         Quando acessa o prontuário desejado
#         Então a conduta crítica deve aparecer com destaque visual.
#         """

#         Conduta.objects.create(
#             consulta=self.consulta,
#             descricao="Iniciar expansão volêmica imediatamente",
#             critica=True
#         )

#         self.login()
#         self.abrir_prontuario()

#         body_text = self.selenium.find_element(By.TAG_NAME, "body").text

#         self.assertIn(
#             "Iniciar expansão volêmica imediatamente",
#             body_text
#         )

#         condutas_criticas = self.selenium.find_elements(
#             By.CLASS_NAME,
#             "conduta-critica"
#         )

#         self.assertGreater(
#             len(condutas_criticas),
#             0,
#             "A conduta crítica deveria aparecer destacada visualmente no prontuário."
#         )

#     def test_conduta_nao_critica_nao_recebe_destaque_visual(self):
#         """
#         Cenário Negativo:

#         Dado que o prontuário do paciente possui condutas registradas,
#         mas nenhuma está marcada como crítica
#         Quando o prontuário é exibido na tela
#         Então nenhuma conduta deve ser destacada visualmente.
#         """

#         Conduta.objects.create(
#             consulta=self.consulta,
#             descricao="Manter observação clínica",
#             critica=False
#         )

#         self.login()
#         self.abrir_prontuario()

#         body_text = self.selenium.find_element(By.TAG_NAME, "body").text

#         self.assertIn(
#             "Manter observação clínica",
#             body_text
#         )

#         condutas_criticas = self.selenium.find_elements(
#             By.CLASS_NAME,
#             "conduta-critica"
#         )

#         self.assertEqual(
#             len(condutas_criticas),
#             0,
#             "Nenhuma conduta deveria receber destaque visual quando não for crítica."
#         )