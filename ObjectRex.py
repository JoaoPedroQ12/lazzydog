import re
import sqlite3

class Capture_date:
    def __init__(self, note):
        self.note = self.read_file(note)
        
    def read_file(self, file):
        with open(file, "r", encoding="latin1") as f:
            content = f.read()
        return content

    def nmov(self):
        m = re.search(r'Nr:\s*(\d+)', self.note)
        return m.group(1) if m else None

    def date(self):
        m = re.search(r'Emissao:\s*(\d{2}/\d{2}/\d{4})', self.note)
        return m.group(1) if m else None

    def client(self):
        m = re.search(r'Cliente\.\:\s*(.+)', self.note)
        return m.group(1).strip() if m else None

    def product(self):
        """Retorna as linhas completas dos produtos"""
        return re.findall(r'(\d{6}\s+.+?\s+UN\s+\w+\s+[\d,.]+\s+[\d,.]+)', self.note)
        
    def code_product(self):
        """Retorna somente os códigos (primeiros 6 dígitos)"""
        produtos = re.findall(r'(\d{6})\s+.+?\s+UN\s+\w+\s+[\d,.]+\s+[\d,.]+', self.note)
        return produtos

    def observ(self):
        m = re.search(r'%%\w%%', self.note)
        return m.group(1) if m else None


class Paint_date(Capture_date): 
    CODES = {
        '020036':'A', '020035':'A', '020034':'A', '020033':'C', '020032':'B', '020031':'A',
        '020030':'C', '020029':'B', '020028':'A', '020027':'C', '020026':'B', '020025':'A',
        '020024':'C', '020023':'B', '020022':'A', '020021':'B', '020020':'A', '020019':'B',
        '020018':'A', '020017':'C', '020016':'B', '020015':'A', '020014':'C', '020013':'B',
        '020012':'A', '020037':'A', '020038':'B', '020039':'C'
    }

    PATH_DB = "latex.sqlite"

    def color(self):
        """Retorna todas as cores encontradas na nota"""
        return re.findall(r'#\w+', self.note)

    def base_produto(self, code: str) -> str:
        """Retorna a base referente ao código da tinta"""
        return self.CODES.get(code, None)            

    def busca_cor(self, color):
        """Busca a base pelo código da cor no banco de dados"""
        resultado = None
        try:
            con = sqlite3.connect(self.PATH_DB)
            cursor = con.cursor()
            cursor.execute("SELECT baseapelid FROM latex WHERE codigo = ?", (color[0],))
            linha = cursor.fetchone()
            if linha:
                resultado = linha[0]
        except Exception as e:
            print(f"Houve um erro na busca_cor: {e}")
        finally:
            if 'con' in locals():
                con.close()
        return resultado

class Database:
    def __init__(self, path_db):
        """Inicializa a conexão com o banco SQLite"""
        self.path_db = path_db
        self.conn = None
        self.cursor = None

    def conectar(self):
        """Abre a conexão com o banco"""
        try:
            self.conn = sqlite3.connect(self.path_db)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao conectar ao banco: {e}")
            return False

    def desconectar(self):
        """Fecha a conexão"""
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"[ERRO] Falha ao fechar o banco: {e}")

    def executar(self, query, params=None):
        """Executa comandos (INSERT, UPDATE, DELETE, etc.)"""
        if not self.cursor:
            print("[AVISO] Conexão não iniciada. Chame conectar() antes.")
            return

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"[ERRO] Falha ao executar comando: {e}")

    def consultar(self, query, params=None):
        """Executa SELECT e retorna os resultados"""
        if not self.cursor:
            print("[AVISO] Conexão não iniciada. Chame conectar() antes.")
            return []

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[ERRO] Falha na consulta: {e}")
            return []
