from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from datetime import date
import time
import os
from usuarios.models import Usuario
from dashboard.models import Prescricao
from dashboard.models import Paciente, Consulta, Medico, PacienteExportado
from protocolos.models import Protocolo
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseSeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1280,960")

        if os.environ.get('GITHUB_ACTIONS') == 'true':
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')

        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(service=service, options=chrome_options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser(
            username="testeteste",
            email="teste@teste.com",
            password="teste123",
            id_acesso="123456",
        )
        self._fazer_login()

    def _fazer_login(self):
        self.selenium.get(self.live_server_url + "/usuarios/login/")
        time.sleep(1)
        self.selenium.find_element(By.ID, "id_acesso").clear()
        self.selenium.find_element(By.ID, "id_acesso").send_keys("123456")
        self.selenium.find_element(By.ID, "password").clear()
        self.selenium.find_element(By.ID, "password").send_keys("teste123")
        self.selenium.find_element(By.CSS_SELECTOR, "[type=submit]").click()
        time.sleep(2)

    def tearDown(self):
        try:
            self.selenium.switch_to.alert.accept()
        except Exception:
            pass

class CalculadoraSeleniumTests(BaseSeleniumTests):  

    def setUp(self):
        super().setUp()  
        self.url_calculadora = self.live_server_url + '/protocolos/calculadora/'

        self.paciente = Paciente.objects.create(
            nome_completo="João Silva",
            data_nascimento="2000-01-01",
            peso=70,
            genero="M",
            altura=1.75,
            nome_mae="Maria Silva",
            nome_pai="José Silva"
        )

        self.consulta = Consulta.objects.create(
            paciente=self.paciente,
            data_consulta=date.today(),
            alergias="Nenhuma",
            doencas_cronicas="Nenhuma",
            cirurgias_anteriores="Nenhuma",
            medicamentos_uso_continuo="Nenhum",
            queixa_principal="Febre",
            historico_de_doenca_atual="Paciente com febre",
            frequencia_respiratoria="20",
            pressao_arterial="120/80",
            frequencia_cardiaca="80",
            temperatura="38",
            saturacao="98",
            ausculta_pulmonar="Normal",
            estado_geral="Regular",
            exames_solicitados="Hemograma",
            diagnostico_provisorio="Suspeita de dengue"
        )

        self.protocolo = Protocolo.objects.create(
            titulo="Dengue",
            descricao="Protocolo de dengue"
        )

    def test_selecionar_paciente_preenche_peso_e_altura_automaticamente(self):
        """Cenário Positivo: Peso e altura preenchidos automaticamente."""
        self.selenium.get(self.url_calculadora)

        select_element = WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, "select-paciente"))
        )

        Select(select_element).select_by_value(str(self.paciente.id))

        WebDriverWait(self.selenium, 5).until(
            lambda d: d.find_element(By.ID, "info-peso").text.strip() != "—"
        )

        peso = self.selenium.find_element(By.ID, "info-peso").text.strip()
        altura = self.selenium.find_element(By.ID, "info-altura").text.strip()

        self.assertNotEqual(peso, "")
        self.assertNotEqual(altura, "")
        self.assertNotEqual(peso, "—")
        self.assertNotEqual(altura, "—")

    def test_selecionar_opcao_vazia_mantem_campos_em_branco(self):
        """Cenário Negativo: Limpar seleção mantém os blocos vazios."""
        self.selenium.get(self.url_calculadora)
        time.sleep(1)

        select_element = WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.ID, "select-paciente"))
        )

        Select(select_element).select_by_value("")
        time.sleep(1)

        peso = self.selenium.find_element(By.ID, "info-peso").text.strip()
        altura = self.selenium.find_element(By.ID, "info-altura").text.strip()

        self.assertTrue(peso in ["", "—"])
        self.assertTrue(altura in ["", "—"])

        resultado = self.selenium.find_element(By.ID, "calculadora-resultado")
        self.assertFalse(resultado.is_displayed())

    def test_modal_mesclar_paciente_abre(self):
        self.selenium.get(self.live_server_url + "/protocolos/detalhes/")

        botao_mesclar = WebDriverWait(self.selenium, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Mesclar paciente')]")
            )
        )
        botao_mesclar.click()

        modal = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.ID, "modal-paciente"))
        )
        self.assertTrue(modal.is_displayed())


class MesclarProtocoloTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user_teste = User.objects.create_superuser(
            username="medico_backend", 
            email="backend@teste.com",
            password="senha_secreta",
            id_acesso="123456" 
        )
        self.client.force_login(self.user_teste)

        self.paciente = Paciente.objects.create(
            nome_completo="João Silva",
            data_nascimento="2000-01-01",
            peso=70, genero="M", altura=1.75,
            nome_mae="Maria Silva", nome_pai="José Silva"
        )

        self.consulta = Consulta.objects.create(
            paciente=self.paciente,
            data_consulta=date.today(),
            alergias="Nenhuma", doencas_cronicas="Nenhuma",
            cirurgias_anteriores="Nenhuma", medicamentos_uso_continuo="Nenhum",
            queixa_principal="Febre", historico_de_doenca_atual="Paciente com febre",
            frequencia_respiratoria="20", pressao_arterial="120/80",
            frequencia_cardiaca="80", temperatura="38", saturacao="98",
            ausculta_pulmonar="Normal", estado_geral="Regular",
            exames_solicitados="Hemograma", diagnostico_provisorio="Suspeita de dengue"
        )

        self.protocolo = Protocolo.objects.create(
            titulo="Dengue",
            descricao="Protocolo de dengue"
        )

    def test_mesclar_protocolo_com_paciente(self):
        url = reverse(
            "mesclar_paciente",
            args=[self.protocolo.id, self.paciente.id]
        )
        response = self.client.get(url)
        self.consulta.refresh_from_db()

        self.assertIn(
            self.protocolo,
            self.consulta.protocolos_utilizados.all()
        )
        self.assertEqual(response.status_code, 302)

    def test_protocolo_aparece_no_prontuario(self):
        self.consulta.protocolos_utilizados.add(self.protocolo)
        url = reverse(
            "prontuario_paciente",
            args=[self.paciente.id]
        )
        response = self.client.get(url)
        self.assertContains(response, "Dengue")


class ExportarPacienteTests(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1280,960')

        if os.environ.get('GITHUB_ACTIONS') == 'true':
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')

        service = Service(ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service, options=chrome_options)
        self.selenium.implicitly_wait(5)

        self.usuario = Usuario.objects.create_superuser(
            username='admin',
            email='admin@teste.com',
            password='admin123',
            id_acesso='123456'
        )
        self.paciente = Paciente.objects.create(
            nome_completo='João Silva',
            data_nascimento='1990-01-15',
            peso=70.0, genero='M', altura=1.75,
            nome_mae='Maria Silva', nome_pai='José Silva',
        )
        self.consulta = Consulta.objects.create(
            paciente=self.paciente,
            data_consulta=date.today(),
            alergias='Nenhuma', doencas_cronicas='Nenhuma',
            cirurgias_anteriores='Nenhuma', medicamentos_uso_continuo='Nenhum',
            queixa_principal='Dor de cabeça',
            historico_de_doenca_atual='Início há 2 dias',
            frequencia_respiratoria='16', pressao_arterial='120/80',
            frequencia_cardiaca='72', temperatura='36.5',
            saturacao='98', ausculta_pulmonar='Normal',
            estado_geral='Bom', exames_solicitados='Hemograma',
            diagnostico_provisorio='Cefaleia tensional',
        )
        self.medico = Medico.objects.create(
            nome='Dr. Teste', crm='99999', especialidade='Clínica Geral'
        )

    def tearDown(self):
        self.selenium.quit()

    def login(self):
        self.selenium.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(1)
        self.selenium.find_element(By.ID, 'id_acesso').clear()
        self.selenium.find_element(By.ID, 'id_acesso').send_keys('123456')
        self.selenium.find_element(By.ID, 'password').clear()
        self.selenium.find_element(By.ID, 'password').send_keys('admin123')
        self.selenium.find_element(By.CSS_SELECTOR, '[type=submit]').click()
        time.sleep(2)

    def abrir_prontuario(self):
        url = reverse('prontuario_paciente', args=[self.paciente.id])
        self.selenium.get(f'{self.live_server_url}{url}')
        time.sleep(2)

    def test_modal_exportar_abre_ao_clicar(self):
        self.login()
        self.abrir_prontuario()

        botao = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick, 'abrirModalExportar')]")
            )
        )
        botao.click()
        time.sleep(1)

        modal = self.selenium.find_element(By.ID, 'modalExportar')
        self.assertEqual(modal.value_of_css_property('display'), 'flex')

    def test_modal_exibe_medico_cadastrado(self):
        self.login()
        self.abrir_prontuario()

        WebDriverWait(self.selenium, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick, 'abrirModalExportar')]")
            )
        ).click()
        time.sleep(0.5)

        lista = self.selenium.find_element(By.ID, 'listaMedicos').text
        self.assertIn('Dr. Teste', lista)

    def test_pesquisa_medico_inexistente_exibe_nenhum_resultado(self):
        self.login()
        self.abrir_prontuario()

        WebDriverWait(self.selenium, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick, 'abrirModalExportar')]")
            )
        ).click()
        time.sleep(0.5)

        campo = self.selenium.find_element(By.ID, 'campoPesquisaMedico')
        campo.send_keys('xyzmedico123')
        time.sleep(0.5)

        aviso = self.selenium.find_element(By.ID, 'nenhumResultado')
        self.assertTrue(aviso.is_displayed())

    def test_exportar_paciente_exibe_toast_confirmacao(self):
        self.login()
        self.abrir_prontuario()

        WebDriverWait(self.selenium, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@onclick, 'abrirModalExportar')]")
            )
        ).click()
        time.sleep(0.5)

        self.selenium.find_element(By.CLASS_NAME, 'medico-item').click()
        time.sleep(0.3)

        self.selenium.find_element(By.CLASS_NAME, 'btn-confirmar').click()
        time.sleep(1.5)

        toast = self.selenium.find_element(By.ID, 'toastConfirmacao')
        self.assertIn('exportado', toast.text.lower())

    def test_exportar_mesmo_medico_duas_vezes_exibe_aviso(self):
        self.login()

        for _ in range(2):
            self.abrir_prontuario()
            WebDriverWait(self.selenium, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@onclick, 'abrirModalExportar')]")
                )
            ).click()
            time.sleep(0.5)
            self.selenium.find_element(By.CLASS_NAME, 'medico-item').click()
            time.sleep(0.3)
            self.selenium.find_element(By.CLASS_NAME, 'btn-confirmar').click()
            time.sleep(1.5)

        toast_erro = self.selenium.find_element(By.ID, 'toastErro')
        self.assertTrue(toast_erro.is_displayed())


class PrescreverMedicamentoTests(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1280,960')

        if os.environ.get('GITHUB_ACTIONS') == 'true':
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')

        service = Service(ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service, options=chrome_options)
        self.selenium.implicitly_wait(5)

        self.usuario = Usuario.objects.create_superuser(
            username='admin2',
            email='admin2@teste.com',
            password='admin123',
            id_acesso='123456'
        )

        self.paciente = Paciente.objects.create(
            nome_completo="Luis Top",
            data_nascimento="2015-05-10",
            peso=35.0, genero="F", altura=140,
            nome_mae="Leticia", nome_pai="Davi"
        )
        
        self.consulta = Consulta.objects.create(
            paciente=self.paciente,
            data_consulta=date.today(),
            queixa_principal="Febre",
            estado_geral="Regular"
        )

    def tearDown(self):
        self.selenium.quit()

    def login(self):
        self.selenium.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(1)
        self.selenium.find_element(By.ID, 'id_acesso').clear()
        self.selenium.find_element(By.ID, 'id_acesso').send_keys('123456')
        self.selenium.find_element(By.ID, 'password').clear()
        self.selenium.find_element(By.ID, 'password').send_keys('admin123')
        self.selenium.find_element(By.CSS_SELECTOR, '[type=submit]').click()
        time.sleep(2)

    def test_fluxo_completo_prescrever_e_bloquear_repetido(self):
        self.login()
        
        self.selenium.get(self.live_server_url + "/protocolos/calculadora/")
        time.sleep(1)

        select_paciente = Select(self.selenium.find_element(By.ID, "select-paciente"))
        select_paciente.select_by_value(str(self.paciente.id))
        time.sleep(2) 

        select_med = Select(self.selenium.find_element(By.ID, "medicacao"))
        select_med.select_by_value("dipirona")
        time.sleep(1) 

        btn_prescrever = self.selenium.find_element(By.ID, "btn-prescrever")
        btn_prescrever.click()
        time.sleep(2) 

        url_prontuario = reverse('prontuario_paciente', args=[self.paciente.id])
        self.selenium.get(self.live_server_url + url_prontuario)
        time.sleep(2) 

        self.selenium.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
        time.sleep(3) 

        body_text = self.selenium.find_element(By.TAG_NAME, "body").text
        self.assertIn("Medicamentos prescritos", body_text)
        self.assertIn("Dipirona", body_text)

        self.selenium.get(self.live_server_url + "/protocolos/calculadora/")
        time.sleep(1)

        select_paciente = Select(self.selenium.find_element(By.ID, "select-paciente"))
        select_paciente.select_by_value(str(self.paciente.id))
        time.sleep(2)

        select_med = Select(self.selenium.find_element(By.ID, "medicacao"))
        select_med.select_by_value("dipirona")
        time.sleep(1)

        btn_prescrever = self.selenium.find_element(By.ID, "btn-prescrever")
        btn_prescrever.click()
        time.sleep(1.5) 

        try:
            toast_erro = WebDriverWait(self.selenium, 3).until(
                EC.visibility_of_element_located((By.ID, "alerta-flutuante"))
            )
            texto_erro = toast_erro.text
            self.assertIn("já está prescrito", texto_erro.lower())
            
        except TimeoutException:
            self.fail("O pop-up (toast) de erro não foi exibido na tela ao tentar prescrever repetido.")


class CadastrarPacienteTests(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1280,960')

        if os.environ.get('GITHUB_ACTIONS') == 'true':
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')

        service = Service(ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service, options=chrome_options)
        self.selenium.implicitly_wait(5)

        self.usuario = Usuario.objects.create_superuser(
            username='medico_intensivista',
            email='medico@teste.com',
            password='admin123',
            id_acesso='123456'
        )

    def tearDown(self):
        self.selenium.quit()

    def login(self):
        self.selenium.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(1)
        self.selenium.find_element(By.ID, 'id_acesso').clear()
        self.selenium.find_element(By.ID, 'id_acesso').send_keys('123456')
        self.selenium.find_element(By.ID, 'password').clear()
        self.selenium.find_element(By.ID, 'password').send_keys('admin123')
        self.selenium.find_element(By.CSS_SELECTOR, '[type=submit]').click()
        time.sleep(2)

    def test_cenario_positivo_cadastrar_novo_paciente(self):
        self.login()
        self.selenium.get(self.live_server_url + "/dashboard/cadastrar/")
        time.sleep(1)

        self.selenium.find_element(By.NAME, "nome_completo").send_keys("Carlos Eduardo")
        time.sleep(0.5)
        self.selenium.find_element(By.NAME, "data_nascimento").send_keys("15/08/1985")
        time.sleep(0.5)
        self.selenium.find_element(By.NAME, "peso").send_keys("80.5")
        time.sleep(0.5)
        self.selenium.find_element(By.NAME, "altura").send_keys("180")
        
        select_genero = Select(self.selenium.find_element(By.NAME, "genero"))
        select_genero.select_by_value("M")
        time.sleep(0.5)

        botao_salvar = self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']")
        botao_salvar.click()
        time.sleep(2) 

        quantidade_pacientes = Paciente.objects.count()
        self.assertEqual(quantidade_pacientes, 1)
        
        paciente_salvo = Paciente.objects.first()
        self.assertEqual(paciente_salvo.nome_completo, "Carlos Eduardo")
        self.assertEqual(float(paciente_salvo.peso), 80.5)

    def test_cenario_negativo_tentar_salvar_sem_dados_obrigatorios(self):
        self.login()
        self.selenium.get(self.live_server_url + "/dashboard/cadastrar/")
        time.sleep(1)

        botao_salvar = self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']")
        botao_salvar.click()
        time.sleep(1.5)

        quantidade_pacientes = Paciente.objects.count()
        self.assertEqual(quantidade_pacientes, 0)

        body_text = self.selenium.find_element(By.TAG_NAME, "body").text
        self.assertIn("obrigatório", body_text.lower())


class ListaProtocolosTests(BaseSeleniumTests):

    def setUp(self):
        if self._testMethodName == 'test_medico_nao_autenticado_e_direcionado_para_login':
            self.selenium.get(self.live_server_url + "/")
            self.selenium.delete_all_cookies()
            self.url_protocolos = self.live_server_url + "/protocolos/"
        else:
            super().setUp()
            self.url_protocolos = self.live_server_url + "/protocolos/"

    def test_medico_autenticado_ve_protocolos_organizados(self):
        self.selenium.get(self.url_protocolos)

        lista = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "lista-protocolos"))
        )
        self.assertTrue(lista.is_displayed())

        cards = self.selenium.find_elements(By.CLASS_NAME, "sub_header")
        visiveis = [c for c in cards if c.is_displayed()]
        self.assertGreater(len(visiveis), 0)

    def test_clicar_em_protocolo_acessa_conteudo_corretamente(self):
        self.selenium.get(self.url_protocolos)

        protocolo = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "sub_header"))
        )
        protocolo.click()

        WebDriverWait(self.selenium, 10).until(
            lambda d: d.current_url != self.url_protocolos
        )
        self.assertNotEqual(self.selenium.current_url, self.url_protocolos)

    def test_medico_nao_autenticado_e_direcionado_para_login(self):
        self.selenium.get(self.live_server_url + "/protocolos/")
        time.sleep(1.5)
        
        WebDriverWait(self.selenium, 10).until(
            EC.url_contains("/login/")
        )
        self.assertIn("/login/", self.selenium.current_url)

    def test_sem_sintoma_informado_exibe_todos_os_protocolos(self):
        self.selenium.get(self.url_protocolos)

        campo_busca = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Buscar protocolos...']")
            )
        )
        self.assertEqual(campo_busca.get_attribute("value"), "")

        todos_os_cards = [
            c for c in self.selenium.find_elements(By.CLASS_NAME, "sub_header") if c.is_displayed()
        ]
        self.assertGreater(len(todos_os_cards), 0)


class FluxogramaTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1280,960")

        if os.environ.get('GITHUB_ACTIONS') == 'true':
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')

        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(service=service, options=chrome_options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser(
            username="testeteste", email="teste@teste.com", password="teste123", id_acesso="123456",
        )
        Protocolo.objects.create(titulo="Dengue", descricao="Protocolo de dengue")
        self._fazer_login()
        self.url_fluxograma = self.live_server_url + "/protocolos/fluxograma/"

    def _fazer_login(self):
        self.selenium.get(self.live_server_url + "/usuarios/login/")
        time.sleep(1)
        self.selenium.find_element(By.ID, "id_acesso").clear()
        self.selenium.find_element(By.ID, "id_acesso").send_keys("123456")
        self.selenium.find_element(By.ID, "password").clear()
        self.selenium.find_element(By.ID, "password").send_keys("teste123")
        self.selenium.find_element(By.CSS_SELECTOR, "[type=submit]").click()
        time.sleep(2)

    def tearDown(self):
        try:
            self.selenium.switch_to.alert.accept()
        except Exception:
            pass

    def test_concluir_etapa_destaca_como_concluida_e_exibe_proxima(self):
        self.selenium.get(self.url_fluxograma)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-fluxo-wrap"))
        )

        self.selenium.find_element(By.CLASS_NAME, "card-fluxo-wrap").click()
        time.sleep(0.5)

        WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-opcao-fluxo"))
        ).click()
        time.sleep(0.5)

        WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-concluir-etapa"))
        ).click()
        time.sleep(0.5)

        card = self.selenium.find_element(By.CLASS_NAME, "card-fluxo-wrap")
        self.assertIn("concluido", card.get_attribute("class"))

        cards = self.selenium.find_elements(By.CLASS_NAME, "card-fluxo-wrap")
        cards_reais = [c for c in cards if "progresso-wrap" not in c.get_attribute("class")]
        self.assertGreater(len(cards_reais), 1)

    def test_proxima_etapa_indisponivel_sem_concluir_anterior(self):
        self.selenium.get(self.url_fluxograma)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-fluxo-wrap"))
        )
        time.sleep(1)

        self.selenium.find_element(By.CLASS_NAME, "card-fluxo-wrap").click()
        time.sleep(0.5)

        btn_concluir = self.selenium.find_element(By.CLASS_NAME, "btn-concluir-etapa")
        self.assertEqual(btn_concluir.get_attribute("disabled"), "true")

        cards = self.selenium.find_elements(By.CLASS_NAME, "card-fluxo-wrap")
        cards_reais = [c for c in cards if "progresso-wrap" not in c.get_attribute("class")]
        self.assertEqual(len(cards_reais), 1)  