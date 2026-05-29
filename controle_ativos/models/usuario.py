class Usuario:
    """
    Classe responsável por representar um usuário do sistema.
    """

    def __init__(
        self,
        usuario_id,
        email,
        senha_hash,
        pergunta_recuperacao,
        resposta_recuperacao_hash,
        perfil="USUARIO",
        ativo=True,
        ultimo_login=None,
        bloqueado_ate=None,
        criado_em=None,
        atualizado_em=None,
    ):
        self.id = usuario_id
        self.email = email
        self.senha_hash = senha_hash
        self.pergunta_recuperacao = pergunta_recuperacao
        self.resposta_recuperacao_hash = resposta_recuperacao_hash
        self.perfil = perfil or "USUARIO"
        self.ativo = bool(ativo)
        self.ultimo_login = ultimo_login
        self.bloqueado_ate = bloqueado_ate
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def to_dict(self):
        """
        Converte o objeto em dicionário sem expor hashes sensíveis.
        """
        return {
            "id": self.id,
            "email": self.email,
            "perfil": self.perfil,
            "ativo": self.ativo,
            "ultimo_login": self.ultimo_login,
            "bloqueado_ate": self.bloqueado_ate,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }