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
from usuarios.models import Usuario
from dashboard.models import Prescricao
from dashboard.models import Paciente, Consulta, Medico, PacienteExportado
from protocolos.models import Protocolo
from django.contrib.auth import get_user_model

User = get_user_model()

class CalculadoraSeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        chrome_options = Options()
        chrome_options.add_argument('--window-size=1280,960')

        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
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

    def tearDown(self):
        try:
            self.selenium.switch_to.alert.accept()
        except:
            pass

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

    """VERIFICAR"""

    # def test_timer_fluxograma_inicia_ao_clicar_na_etapa(self):
    #     self.selenium.get(self.live_server_url + "/protocolos/fluxograma/")

    #     primeiro_card = WebDriverWait(self.selenium, 5).until(
    #         EC.element_to_be_clickable((By.CLASS_NAME, "card-fluxo-wrap"))
    #     )

    #     timer = self.selenium.find_element(By.ID, "timer-etapa-0")

    #     self.assertEqual(timer.text.strip(), "00:00")

    #     primeiro_card.click()

    #     time.sleep(2)

    #     self.assertNotEqual(timer.text.strip(), "00:00")

    """VERIFICAR"""

    # def test_timer_para_ao_concluir_etapa(self):
    #     self.selenium.get(self.live_server_url + "/protocolos/fluxograma/")

    #     primeiro_card = WebDriverWait(self.selenium, 5).until(
    #         EC.element_to_be_clickable((By.CLASS_NAME, "card-fluxo-wrap"))
    #     )

    #     primeiro_card.click()

    #     time.sleep(2)

    #     botao_concluir = self.selenium.find_element(
    #         By.CLASS_NAME,
    #         "btn-concluir-etapa"
    #     )

    #     botao_concluir.click()

    #     timer = self.selenium.find_element(By.ID, "timer-etapa-0")
    #     tempo_parado = timer.text.strip()

    #     time.sleep(2)

    #     self.assertEqual(timer.text.strip(), tempo_parado)


class MesclarProtocoloTests(TestCase):

    def setUp(self):
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

#testes de exportar paciente
class ExportarPacienteTests(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1280,960')
        service = Service(ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service, options=chrome_options)
        self.selenium.implicitly_wait(5)

        from usuarios.models import Usuario
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
        from django.urls import reverse
        url = reverse('prontuario_paciente', args=[self.paciente.id])
        self.selenium.get(f'{self.live_server_url}{url}')
        time.sleep(2)

    def test_modal_exportar_abre_ao_clicar(self):
        """O modal de exportar deve abrir ao clicar no botão."""
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
        """O modal deve listar o médico cadastrado."""
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
        """Pesquisar médico inexistente deve exibir 'Nenhum resultado'."""
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
        """Ao confirmar exportação deve aparecer o toast de sucesso."""
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
        """Exportar para o mesmo médico duas vezes deve exibir aviso de erro."""
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
        service = Service(ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service, options=chrome_options)
        self.selenium.implicitly_wait(5)

        from usuarios.models import Usuario
        self.usuario = Usuario.objects.create_superuser(
            username='admin2',
            email='admin2@teste.com',
            password='admin123',
            id_acesso='123456'
        )

        self.paciente = Paciente.objects.create(
            nome_completo="Luis Top",
            data_nascimento="2015-05-10",
            peso=35.0, 
            genero="F", 
            altura=140,
            nome_mae="Leticia", 
            nome_pai="Davi"
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
        """Verifica o sucesso da prescrição, rola a página do prontuário, e depois testa o bloqueio de repetição."""
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

        # Preenche tudo de novo
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
        # 1. Configuração do Chrome
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1280,960')
        service = Service(ChromeDriverManager().install())
        self.selenium = webdriver.Chrome(service=service, options=chrome_options)
        self.selenium.implicitly_wait(5)

        from usuarios.models import Usuario
        self.usuario = Usuario.objects.create_superuser(
            username='medico_intensivista',
            email='medico@teste.com',
            password='admin123',
            id_acesso='123456'
        )

    def tearDown(self):
        self.selenium.quit()

    def login(self):
        """Função auxiliar para o robô fazer o login antes de testar"""
        self.selenium.get(f'{self.live_server_url}/usuarios/login/')
        time.sleep(1)
        self.selenium.find_element(By.ID, 'id_acesso').clear()
        self.selenium.find_element(By.ID, 'id_acesso').send_keys('123456')
        self.selenium.find_element(By.ID, 'password').clear()
        self.selenium.find_element(By.ID, 'password').send_keys('admin123')
        self.selenium.find_element(By.CSS_SELECTOR, '[type=submit]').click()
        time.sleep(2)

    def test_cenario_positivo_cadastrar_novo_paciente(self):
        """
        Cenário Positivo:
        Dado que o médico está cadastrado no sistema
        Quando o médico abre a tela de cadastro e informa os dados do novo paciente
        Então o sistema salva as informações e redireciona com sucesso
        """
        self.login()
        
        self.selenium.get(self.live_server_url + "/dashboard/cadastrar/")
        time.sleep(1)

        self.selenium.find_element(By.NAME, "nome_completo").send_keys("Carlos Eduardo")
        self.selenium.find_element(By.NAME, "data_nascimento").send_keys("15/08/1985")
        self.selenium.find_element(By.NAME, "peso").send_keys("80.5")
        self.selenium.find_element(By.NAME, "altura").send_keys("180")
        
        select_genero = Select(self.selenium.find_element(By.NAME, "genero"))
        select_genero.select_by_value("M")

        botao_salvar = self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']")
        botao_salvar.click()
        time.sleep(2) 

        quantidade_pacientes = Paciente.objects.count()
        self.assertEqual(quantidade_pacientes, 1)
        
        paciente_salvo = Paciente.objects.first()
        self.assertEqual(paciente_salvo.nome_completo, "Carlos Eduardo")
        self.assertEqual(float(paciente_salvo.peso), 80.5)

    def test_cenario_negativo_tentar_salvar_sem_dados_obrigatorios(self):
        """
        Cenário Negativo:
        Dado que o médico está na tela de cadastro
        Quando tenta salvar o cadastro do paciente sem os dados obrigatórios
        Então o sistema deve exibir mensagem de erro e não salva o registro
        """
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

class BaseSeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1280,960")
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

class ListaProtocolosTests(BaseSeleniumTests):

    def setUp(self):
        super().setUp()
        self.url_protocolos = self.live_server_url + "/protocolos/"

    def test_medico_autenticado_ve_protocolos_organizados(self):
        """
        Dado que o médico está autenticado no sistema e existem protocolos
        clínicos cadastrados,
        Quando o médico acessa a seção de protocolos,
        Então o sistema deve exibir os protocolos organizados por categoria
        ou especialidade, permitindo navegação rápida e acesso ao conteúdo
        de cada protocolo corretamente.
        """
        self.selenium.get(self.url_protocolos)

        lista = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, "lista-protocolos"))
        )
        self.assertTrue(lista.is_displayed(), "A lista de protocolos deveria estar visível.")

        cards = self.selenium.find_elements(By.CLASS_NAME, "sub_header")
        visiveis = [c for c in cards if c.is_displayed()]
        self.assertGreater(len(visiveis), 0, "Nenhum protocolo foi renderizado na lista.")

    def test_clicar_em_protocolo_acessa_conteudo_corretamente(self):
        """
        Dado que o médico está autenticado no sistema e existem protocolos
        clínicos cadastrados,
        Quando o médico acessa a seção de protocolos,
        Então o sistema deve permitir acesso ao conteúdo de cada protocolo
        corretamente.
        """
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
        """
        Dado que o médico não está autenticado no sistema,
        Quando o médico tenta acessar a seção de protocolos,
        Então o sistema deve direcioná-lo para a tela de login.
        """
        self.selenium.get(self.live_server_url + "/usuarios/logout/")
        time.sleep(1)

        self.selenium.get(self.url_protocolos)
        time.sleep(2)

        self.assertIn("/login/", self.selenium.current_url)

    def test_sem_sintoma_informado_exibe_todos_os_protocolos(self):
        """
        Dado que o médico está autenticado no sistema,
        Quando o médico informa nenhum sintoma do paciente,
        Então o sistema deve exibir todos os protocolos existentes.
        """
        self.selenium.get(self.url_protocolos)

        campo_busca = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Buscar protocolos...']")
            )
        )
        self.assertEqual(campo_busca.get_attribute("value"), "")

        todos_os_cards = [
            c
            for c in self.selenium.find_elements(By.CLASS_NAME, "sub_header")
            if c.is_displayed()
        ]
        self.assertGreater(
            len(todos_os_cards),
            0,
            "Com campo vazio, todos os protocolos existentes deveriam ser exibidos.",
        )

class FluxogramaTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1280,960")
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
        Protocolo.objects.create(
            titulo="Dengue",
            descricao="Protocolo de dengue"
        )
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
        """
        Dado que o médico está visualizando um protocolo médico em formato
        de fluxograma interativo,
        Quando ele conclui uma etapa do atendimento e marca a opção de check
        correspondente,
        Então o sistema deve destacar visualmente a etapa como concluída e
        permitir ver o avanço para as próximas etapas do protocolo.
        """
        self.selenium.get(self.url_fluxograma)
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-fluxo-wrap"))
        )

        #ativa o card (inicia timer)
        self.selenium.find_element(By.CLASS_NAME, "card-fluxo-wrap").click()
        time.sleep(0.5)

        #seleciona a primeira alternativa
        WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-opcao-fluxo"))
        ).click()
        time.sleep(0.5)

        #conclui a etapa
        WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-concluir-etapa"))
        ).click()
        time.sleep(0.5)

        #verifica 'concluido' no card
        card = self.selenium.find_element(By.CLASS_NAME, "card-fluxo-wrap")
        self.assertIn("concluido", card.get_attribute("class"))

        #verifica que a próxima etapa apareceu
        cards = self.selenium.find_elements(By.CLASS_NAME, "card-fluxo-wrap")
        cards_reais = [c for c in cards if "progresso-wrap" not in c.get_attribute("class")]
        self.assertGreater(len(cards_reais), 1)

    def test_proxima_etapa_indisponivel_sem_concluir_anterior(self):
        """
        Dado que o médico está utilizando um protocolo médico em formato
        de fluxograma interativo,
        Quando ele tenta acessar uma etapa subsequente sem concluir a etapa
        obrigatória anterior,
        Então o sistema deve manter as próximas etapas indisponíveis para
        interação, sem exibir mensagens de erro ou pop-ups, até que a etapa
        pendente seja concluída.
        """
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