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
from django.contrib.auth import get_user_model
import time

class ProtocolosSeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        chrome_options = Options()
        chrome_options.add_argument('--window-size=1280,960')

        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(service=service, options=chrome_options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.url_protocolos = self.live_server_url + '/protocolos/'
        self.url_fluxograma = self.live_server_url + '/protocolos/fluxograma/'
        User = get_user_model()
        User.objects.create_user(
            username='testeteste',
            email='teste@teste.com',
            password='teste123',
            id_acesso='123456'
        )

        self.selenium.get(self.live_server_url + '/usuarios/login/')
        self.selenium.find_element(By.NAME, 'id_acesso').send_keys('123456')
        self.selenium.find_element(By.NAME, 'password').send_keys('teste123')
        self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

    def tearDown(self):
        try:
            self.selenium.switch_to.alert.accept()
        except:
            pass

    def test_nao_autenticado_redireciona_para_login(self):
        self.selenium.get(self.live_server_url + '/usuarios/logout/')
        time.sleep(1)
        self.selenium.get(self.url_protocolos)
        WebDriverWait(self.selenium, 5).until(
            EC.url_contains('/usuarios/login/')
        )
        self.assertIn('/usuarios/login/', self.selenium.current_url)
        
    def test_lista_protocolos_aparece(self):
        """
        Testa se a lista de protocolos é exibida
        """
        self.selenium.get(self.url_protocolos)
        time.sleep(1)

        try:
            lista = WebDriverWait(self.selenium, 5).until(
                EC.presence_of_element_located((By.ID, "lista-protocolos"))
            )
            self.assertTrue(lista.is_displayed())
        except TimeoutException:
            self.fail("Lista de protocolos não apareceu.")

    def test_cards_de_protocolos_sao_exibidos(self):
        """
        Garante que existem protocolos renderizados
        """
        self.selenium.get(self.url_protocolos)
        time.sleep(1)

        try:
            cards = WebDriverWait(self.selenium, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "sub_header"))
            )
            self.assertTrue(len(cards) > 0)
        except TimeoutException:
            self.fail("Nenhum protocolo foi exibido.")

    def test_busca_filtra_protocolos(self):
        """
        Garante filtro
        """

        self.selenium.get(self.url_protocolos)
        time.sleep(1)

        campo_busca = self.selenium.find_element(
            By.CSS_SELECTOR, "input[placeholder='Buscar protocolos...']"
        )

        campo_busca.send_keys("Dengue")
        time.sleep(1)

        cards = self.selenium.find_elements(By.CLASS_NAME, "sub_header")
        visiveis = [c for c in cards if c.is_displayed()]

        self.assertTrue(len(visiveis) > 0)

    def test_busca_vazia_impede_filtro(self):
        self.selenium.get(self.url_protocolos)
        time.sleep(1)
        self.selenium.find_element(By.ID, "abrirFiltro").click()
        time.sleep(1)
        self.selenium.find_element(By.CLASS_NAME, "btn-aplicar").click()
        time.sleep(1)
        modal = self.selenium.find_element(By.ID, "modal-filtro")
        self.assertIn("ativo", modal.get_attribute("class"))


    def test_clicar_protocolo_abre_detalhes(self):
        """
        Testa se, ao clicar em um protocolo, é redirecionado para a página de detalhes
        """

        self.selenium.get(self.url_protocolos)
        time.sleep(1)

        protocolo = WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sub_header"))
        )

        protocolo.click()
        time.sleep(2)

        WebDriverWait(self.selenium, 5).until(
            EC.url_contains('/detalhes')
        )

        self.assertIn('/detalhes', self.selenium.current_url)

    def test_fluxograma_carrega(self):
        """
        Testa fluxograma
        """

        self.selenium.get(self.url_fluxograma)

        try:
            lista = WebDriverWait(self.selenium, 5).until(
                EC.presence_of_element_located((By.ID, "lista-fluxograma"))
            )
            self.assertTrue(lista.is_displayed())
        except TimeoutException:
            self.fail("Fluxograma não carregou.")
    
    def test_marcar_etapa_destaca_como_concluida(self):
        self.selenium.get(self.url_fluxograma)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-fluxo-wrap"))
        )
        self.selenium.find_element(By.CLASS_NAME, "card-fluxo-wrap").click()
        time.sleep(1)
        primeiro_card = self.selenium.find_element(By.CLASS_NAME, "card-fluxo-wrap")
        self.assertIn("concluido", primeiro_card.get_attribute("class"))

    def test_etapa_seguinte_bloqueada_sem_popup(self):
        self.selenium.get(self.url_fluxograma)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card-fluxo-wrap"))
        )
        cards = self.selenium.find_elements(By.CLASS_NAME, "card-fluxo-wrap")
        cards[1].click()
        time.sleep(1)
        modal = self.selenium.find_element(By.ID, "modal-etapa-pulada")
        self.assertEqual(modal.value_of_css_property("display"), "flex")
