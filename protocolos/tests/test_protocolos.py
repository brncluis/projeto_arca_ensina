from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time

class CalculadoraSeleniumTests(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        
        chrome_options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(service=service, options=chrome_options)
        
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.url_calculadora = self.live_server_url + '/protocolos/calculadora/'
    
    def tearDown(self):
        """Roda após cada teste para fechar qualquer alerta que tenha ficado travado."""
        try:
            self.selenium.switch_to.alert.accept()
        except:
            pass

    def test_alerta_erro_ao_calcular_sem_peso(self):
        """
        Tenta calcular selecionando a medicação, mas sem informar o peso.
        Deve exibir um alert() nativo do navegador.
        """
        self.selenium.get(self.url_calculadora)

        select_element = WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, "medicacao"))
        )
        campo_medicacao = Select(select_element)
        time.sleep(2) 
        campo_medicacao.select_by_index(1) 

        btn_calcular = self.selenium.find_element(By.ID, "btn-calcular")
        btn_calcular.click()

        try:
            alerta = WebDriverWait(self.selenium, 3).until(EC.alert_is_present())
            texto_do_alerta = alerta.text
            
            self.assertEqual(texto_do_alerta, "Preencha o peso e selecione uma medicação.")
            
            alerta.accept()
            time.sleep(2)
            
        except TimeoutException:
            self.fail("O alerta nativo de erro não foi exibido na tela.")

    def test_popup_sucesso_verde_ao_preencher_tudo(self):
        """
        Preenche peso e seleciona medicamento.
        Deve exibir a div verde (alerta-sucesso-flutuante).
        """
        self.selenium.get(self.url_calculadora)

        campo_peso = self.selenium.find_element(By.ID, "peso")
        campo_peso.send_keys("50.5")

        campo_altura = self.selenium.find_element(By.ID, "altura")
        campo_altura.send_keys("130")

        campo_medicacao = Select(self.selenium.find_element(By.ID, "medicacao"))
        time.sleep(2)
        campo_medicacao.select_by_value("dipirona") 

        btn_calcular = self.selenium.find_element(By.ID, "btn-calcular")
        btn_calcular.click()

        try:
            div_sucesso = WebDriverWait(self.selenium, 3).until(
                EC.visibility_of_element_located((By.ID, "alerta-sucesso-flutuante"))
            )
            
            self.assertIn("Cálculo realizado com sucesso!", div_sucesso.text)
            time.sleep(5)
            
        except TimeoutException:
            self.fail("A div verde de sucesso não apareceu ou não recebeu a classe correta.")