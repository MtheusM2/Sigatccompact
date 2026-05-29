import mysql.connector

from controle_ativos.models.ativos import Ativo
from controle_ativos.database.connection import cursor_mysql
from controle_ativos.utils.validators import (
    STATUS_VALIDOS,
    validar_ativo,
    validar_id_ativo,
    padronizar_texto,
    validar_data_iso_opcional
)


class AtivoErro(Exception):
    """Erro base relacionado a ativos."""


class AtivoJaExiste(AtivoErro):
    """Erro para ativo duplicado."""


class AtivoNaoEncontrado(AtivoErro):
    """Erro para ativo inexistente."""


class PermissaoNegada(AtivoErro):
    """Erro para acesso não autorizado."""


def _row_para_ativo(row: dict) -> Ativo:
    """
    Converte uma linha do banco em objeto Ativo.
    """
    return Ativo(
        id_ativo=row["id"],
        tipo=row["tipo"],
        marca=row["marca"],
        modelo=row["modelo"],
        email_responsavel=row.get("email_responsavel"),
        usuario_responsavel=row["usuario_responsavel"],
        departamento=row["departamento"],
        status=row["status"],
        data_entrada=str(row["data_entrada"]),
        data_saida=str(row["data_saida"]) if row["data_saida"] else None,
        criado_por=row["criado_por"]
    )


def _padronizar_ativo(ativo: Ativo) -> Ativo:
    """
    Padroniza campos textuais do ativo antes da persistência.
    """
    return Ativo(
        id_ativo=ativo.id_ativo.strip(),
        tipo=padronizar_texto(ativo.tipo, "title"),
        marca=padronizar_texto(ativo.marca, "title"),
        modelo=padronizar_texto(ativo.modelo, "upper"),
        email_responsavel=(ativo.email_responsavel or "").strip().lower() or None,
        usuario_responsavel=padronizar_texto(ativo.usuario_responsavel, "title"),
        departamento=padronizar_texto(ativo.departamento, "title"),
        status=padronizar_texto(ativo.status, "title"),
        data_entrada=(ativo.data_entrada or "").strip(),
        data_saida=(ativo.data_saida or "").strip() or None,
        criado_por=ativo.criado_por
    )


def _valor_filtro_util(valor):
    if valor is None:
        return None

    valor_limpo = str(valor).strip()
    if not valor_limpo or valor_limpo.lower() == "todos":
        return None

    return valor_limpo


class AtivosService:
    """
    Serviço responsável pelas regras de negócio e persistência dos ativos.
    """

    def criar_ativo(self, ativo: Ativo, user_id: int) -> None:
        _ = user_id
        ativo.criado_por = user_id
        ativo_norm = _padronizar_ativo(ativo)

        try:
            validar_ativo(ativo_norm)
        except ValueError as erro:
            raise AtivoErro(str(erro)) from erro

        with cursor_mysql(dictionary=True) as (_conn, cur):
            try:
                cur.execute(
                    """
                    INSERT INTO ativos (
                        id, tipo, marca, modelo, email_responsavel, usuario_responsavel,
                        departamento, status, data_entrada, data_saida, criado_por
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        ativo_norm.id_ativo,
                        ativo_norm.tipo,
                        ativo_norm.marca,
                        ativo_norm.modelo,
                        ativo_norm.email_responsavel,
                        ativo_norm.usuario_responsavel,
                        ativo_norm.departamento,
                        ativo_norm.status,
                        ativo_norm.data_entrada,
                        ativo_norm.data_saida,
                        user_id
                    )
                )
            except mysql.connector.IntegrityError as erro:
                if getattr(erro, "errno", None) == 1062:
                    raise AtivoJaExiste("Já existe um ativo cadastrado com este ID.") from erro
                raise

    def listar_ativos(self, user_id: int) -> list[Ativo]:
        _ = user_id
        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                """
                  SELECT id, tipo, marca, modelo, email_responsavel, usuario_responsavel,
                       departamento, status, data_entrada, data_saida, criado_por
                FROM ativos
                ORDER BY id
                """,
                (),  # sem parametros
            )
            rows = cur.fetchall()

        return [_row_para_ativo(row) for row in rows]

    def buscar_ativo(self, id_ativo: str, user_id: int) -> Ativo:
        _ = user_id
        ok, msg = validar_id_ativo(id_ativo)
        if not ok:
            raise AtivoErro(msg)

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                """
                  SELECT id, tipo, marca, modelo, email_responsavel, usuario_responsavel,
                       departamento, status, data_entrada, data_saida, criado_por
                FROM ativos
                WHERE id = %s
                """,
                (id_ativo.strip(),)
            )
            row = cur.fetchone()

        if row is None:
            raise AtivoNaoEncontrado("Ativo não encontrado.")

        return _row_para_ativo(row)

    def filtrar_ativos(
        self,
        user_id: int,
        filtros: dict,
        ordenar_por: str = "id",
        ordem: str = "asc"
    ) -> list[Ativo]:
        _ = user_id
        filtros = filtros or {}
        campos_ordenacao = {
            "id": "id",
            "tipo": "tipo",
            "marca": "marca",
            "modelo": "modelo",
            "email_responsavel": "email_responsavel",
            "usuario_responsavel": "usuario_responsavel",
            "departamento": "departamento",
            "status": "status",
            "data_entrada": "data_entrada",
            "data_saida": "data_saida"
        }

        if ordenar_por not in campos_ordenacao:
            raise AtivoErro("Campo de ordenação inválido.")

        ordem_sql = "ASC" if ordem.lower() == "asc" else "DESC"

        where = ["1 = 1"]  # busca global com filtros opcionais
        params = []

        filtros_textuais = {
            "id_ativo": ("id = %s", False),
            "tipo": ("tipo LIKE %s", False),
            "marca": ("marca LIKE %s", False),
            "modelo": ("modelo LIKE %s", False),
            "email_responsavel": ("email_responsavel LIKE %s", True),
            "usuario_responsavel": ("usuario_responsavel LIKE %s", False),
            "departamento": ("departamento LIKE %s", False),
        }

        for chave, (sql_fragmento, normalizar_lower) in filtros_textuais.items():
            valor = _valor_filtro_util(filtros.get(chave))
            if valor is None:
                continue

            if chave == "id_ativo":
                where.append(sql_fragmento)
                params.append(valor)
            else:
                if normalizar_lower:
                    valor = valor.lower()
                where.append(sql_fragmento)
                params.append(f"%{valor}%")

        status = _valor_filtro_util(filtros.get("status"))
        if status is not None:
            status_padronizado = padronizar_texto(status, "title")
            if status_padronizado not in STATUS_VALIDOS:
                raise AtivoErro("Status inválido para filtro.")
            where.append("status = %s")
            params.append(status_padronizado)

        for campo in ["data_entrada_inicial", "data_entrada_final", "data_saida_inicial", "data_saida_final"]:
            valor = _valor_filtro_util(filtros.get(campo))
            ok, msg = validar_data_iso_opcional(valor)
            if not ok:
                raise AtivoErro(msg)

        if _valor_filtro_util(filtros.get("data_entrada_inicial")):
            where.append("data_entrada >= %s")
            params.append(_valor_filtro_util(filtros.get("data_entrada_inicial")))

        if _valor_filtro_util(filtros.get("data_entrada_final")):
            where.append("data_entrada <= %s")
            params.append(_valor_filtro_util(filtros.get("data_entrada_final")))

        if _valor_filtro_util(filtros.get("data_saida_inicial")):
            where.append("data_saida >= %s")
            params.append(_valor_filtro_util(filtros.get("data_saida_inicial")))

        if _valor_filtro_util(filtros.get("data_saida_final")):
            where.append("data_saida <= %s")
            params.append(_valor_filtro_util(filtros.get("data_saida_final")))

        sql = f"""
                 SELECT id, tipo, marca, modelo, email_responsavel, usuario_responsavel,
                   departamento, status, data_entrada, data_saida, criado_por
            FROM ativos
            WHERE {" AND ".join(where)}
            ORDER BY {campos_ordenacao[ordenar_por]} {ordem_sql}
        """

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()

        return [_row_para_ativo(row) for row in rows]

    def atualizar_ativo(self, id_ativo: str, dados: dict, user_id: int) -> Ativo:
        _ = user_id
        atual = self.buscar_ativo(id_ativo=id_ativo, user_id=user_id)

        novo = Ativo(
            id_ativo=atual.id_ativo,
            tipo=dados.get("tipo", atual.tipo),
            marca=dados.get("marca", atual.marca),
            modelo=dados.get("modelo", atual.modelo),
            email_responsavel=dados.get("email_responsavel", getattr(atual, "email_responsavel", None)),
            usuario_responsavel=dados.get("usuario_responsavel", atual.usuario_responsavel),
            departamento=dados.get("departamento", atual.departamento),
            status=dados.get("status", atual.status),
            data_entrada=dados.get("data_entrada", atual.data_entrada),
            data_saida=dados.get("data_saida", atual.data_saida),
            criado_por=atual.criado_por
        )

        novo_norm = _padronizar_ativo(novo)

        try:
            validar_ativo(novo_norm)
        except ValueError as erro:
            raise AtivoErro(str(erro)) from erro

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                """
                UPDATE ativos
                SET tipo=%s,
                    marca=%s,
                    modelo=%s,
                    email_responsavel=%s,
                    usuario_responsavel=%s,
                    departamento=%s,
                    status=%s,
                    data_entrada=%s,
                    data_saida=%s
                WHERE id=%s  # edicao global por id
                """,
                (
                    novo_norm.tipo,
                    novo_norm.marca,
                    novo_norm.modelo,
                    novo_norm.email_responsavel,
                    novo_norm.usuario_responsavel,
                    novo_norm.departamento,
                    novo_norm.status,
                    novo_norm.data_entrada,
                    novo_norm.data_saida,
                    novo_norm.id_ativo,
                )
            )

            if cur.rowcount == 0:
                raise AtivoNaoEncontrado("Não foi possível atualizar o ativo.")

        return novo_norm

    def remover_ativo(self, id_ativo: str, user_id: int) -> None:
        _ = user_id
        ok, msg = validar_id_ativo(id_ativo)
        if not ok:
            raise AtivoErro(msg)

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                "DELETE FROM ativos WHERE id = %s",  # exclusao global por id
                (id_ativo.strip(),)  # apenas o identificador
            )

            if cur.rowcount == 0:
                raise AtivoNaoEncontrado("Não foi possível remover o ativo.")