class Ativo:
    """
    Representa um ativo do sistema.
    """

    def __init__(
        self,
        id_ativo,
        tipo,
        marca,
        modelo,
        usuario_responsavel,
        departamento,
        status,
        data_entrada,
        data_saida=None,
        email_responsavel=None,
        criado_por=None
    ):
        self.id_ativo = id_ativo
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.usuario_responsavel = usuario_responsavel
        self.departamento = departamento
        self.status = status
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.email_responsavel = email_responsavel
        self.criado_por = criado_por
        # empresa_id reservado para futura evolução multi-tenant.

    def to_dict(self):
        """
        Converte o objeto em dicionário.
        """
        return {
            "id_ativo": self.id_ativo,
            "tipo": self.tipo,
            "marca": self.marca,
            "modelo": self.modelo,
            "email_responsavel": self.email_responsavel,
            "usuario_responsavel": self.usuario_responsavel,
            "departamento": self.departamento,
            "status": self.status,
            "data_entrada": self.data_entrada,
            "data_saida": self.data_saida,
            "criado_por": self.criado_por
        }