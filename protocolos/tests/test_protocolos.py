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

    def test_alerta_erro_ao_calcular_sem_peso(self):
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
            alerta = WebDriverWait(self.selenium, 3).until(
                EC.alert_is_present()
            )

            texto_do_alerta = alerta.text

            self.assertEqual(
                texto_do_alerta,
                "Preencha o peso e selecione uma medicação."
            )

            alerta.accept()

        except TimeoutException:
            self.fail("O alerta nativo de erro não foi exibido na tela.")

    def test_popup_sucesso_verde_ao_preencher_tudo(self):
        self.selenium.get(self.url_calculadora)

        campo_peso = self.selenium.find_element(By.ID, "peso")
        campo_peso.send_keys("50.5")

        campo_altura = self.selenium.find_element(By.ID, "altura")
        campo_altura.send_keys("130")

        campo_medicacao = Select(
            self.selenium.find_element(By.ID, "medicacao")
        )

        time.sleep(2)
        campo_medicacao.select_by_value("dipirona")

        btn_calcular = self.selenium.find_element(By.ID, "btn-calcular")
        btn_calcular.click()

        try:
            div_sucesso = WebDriverWait(self.selenium, 3).until(
                EC.visibility_of_element_located(
                    (By.ID, "alerta-sucesso-flutuante")
                )
            )

            self.assertIn(
                "Cálculo realizado com sucesso!",
                div_sucesso.text
            )

        except TimeoutException:
            self.fail("A div verde de sucesso não apareceu.")

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

    def test_timer_fluxograma_inicia_ao_clicar_na_etapa(self):
        self.selenium.get(self.live_server_url + "/protocolos/fluxograma/")

        primeiro_card = WebDriverWait(self.selenium, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "card-fluxo-wrap"))
        )

        timer = self.selenium.find_element(By.ID, "timer-etapa-0")

        self.assertEqual(timer.text.strip(), "00:00")

        primeiro_card.click()

        time.sleep(2)

        self.assertNotEqual(timer.text.strip(), "00:00")

    def test_timer_para_ao_concluir_etapa(self):
        self.selenium.get(self.live_server_url + "/protocolos/fluxograma/")

        primeiro_card = WebDriverWait(self.selenium, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "card-fluxo-wrap"))
        )

        primeiro_card.click()

        time.sleep(2)

        botao_concluir = self.selenium.find_element(
            By.CLASS_NAME,
            "btn-concluir-etapa"
        )

        botao_concluir.click()

        timer = self.selenium.find_element(By.ID, "timer-etapa-0")
        tempo_parado = timer.text.strip()

        time.sleep(2)

        self.assertEqual(timer.text.strip(), tempo_parado)


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