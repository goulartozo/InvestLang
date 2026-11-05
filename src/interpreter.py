
# ==========================================
# INVESTLANG - INTERPRETADOR
# ==========================================

class Interpreter:

    def __init__(self, ast):
        self.ast = ast
        self.carteira = {}
        self.resultados = []
        self.capital = 0

    # ======================================
    # EXECUÇÃO PRINCIPAL
    # ======================================

    def execute(self):

        if not self.ast:
            print("Erro: AST vazia.")
            return

        self.process_statements(self.ast["statements"])

        self.validate_capital()
        self.validate_allocations()
        self.validate_diversification()
        self.validate_restrictions()

        self.show_results()

        return {
            "carteira": self.carteira,
            "resultados": self.resultados
        }

    # ======================================
    # PROCESSAMENTO DAS DECLARAÇÕES
    # ======================================

    def process_statements(self, statements, scope="global"):

        for statement in statements:

            statement_type = statement["type"]

            if statement_type == "assignment":

                name = statement["name"]
                value = statement["value"]

                if scope not in self.carteira:
                    self.carteira[scope] = {}

                self.carteira[scope][name] = value

                if name == "capital_total":
                    self.capital = value["value"]

            elif statement_type == "section":

                self.process_statements(
                    statement["statements"],
                    statement["name"]
                )

            elif statement_type == "conditional":

                if self.evaluate_condition(statement["condition"]):
                    self.process_statements(
                        statement["statements"],
                        scope
                    )

            elif statement_type == "print":

                print(statement["value"]["value"])

            elif statement_type == "command":

                if statement["name"] == "analisar":
                    print("Comando de análise identificado.")

                elif statement["name"] == "gerar_relatorio":
                    print("Comando de geração de relatório identificado.")

    # ======================================
    # AVALIAÇÃO DE CONDIÇÕES
    # ======================================

    def evaluate_condition(self, condition):

        name = condition["left"]
        operator = condition["operator"]
        right = condition["right"]["value"]

        left = self.get_value(name)

        if left is None:
            self.results_error(
                f"Variável '{name}' não encontrada."
            )
            return False

        operations = {
            "==": lambda: left == right,
            "!=": lambda: left != right,
            "<": lambda: left < right,
            ">": lambda: left > right,
            "<=": lambda: left <= right,
            ">=": lambda: left >= right
        }

        return operations[operator]()

    def get_value(self, name):

        for scope in self.carteira.values():

            if name in scope:
                return scope[name]["value"]

        return None

    # ======================================
    # VALIDAÇÃO DO CAPITAL
    # ======================================

    def validate_capital(self):

        if self.capital <= 0:
            self.results_error(
                "O capital total deve ser maior que zero."
            )
        else:
            self.results_success(
                f"Capital total válido: R$ {self.capital:,.2f}"
            )

    # ======================================
    # VALIDAÇÃO DA ALOCAÇÃO
    # ======================================

    def validate_allocations(self):

        allocation = self.carteira.get("alocacao", {})

        if not allocation:
            self.results_error(
                "Nenhuma alocação foi informada."
            )
            return

        total = sum(
            item["value"]
            for item in allocation.values()
            if item["type"] == "percentage"
        )

        if abs(total - 100) < 0.000001:
            self.results_success(
                "A alocação totaliza 100%."
            )
        else:
            self.results_error(
                f"A alocação totaliza {total}%, e não 100%."
            )

        print("\nDISTRIBUIÇÃO DA CARTEIRA")

        for name, item in allocation.items():

            percentage = item["value"]

            value = self.capital * percentage / 100

            print(
                f"{name}: {percentage}% "
                f"= R$ {value:,.2f}"
            )

    # ======================================
    # VALIDAÇÃO DA DIVERSIFICAÇÃO
    # ======================================

    def validate_diversification(self):

        sections = ["setorial", "geografico"]

        for section_name in sections:

            section = self.carteira.get(section_name, {})

            if not section:
                continue

            total = sum(
                item["value"]
                for item in section.values()
                if item["type"] == "percentage"
            )

            if abs(total - 100) < 0.000001:
                self.results_success(
                    f"A diversificação {section_name} totaliza 100%."
                )
            else:
                self.results_error(
                    f"A diversificação {section_name} "
                    f"totaliza {total}%, e não 100%."
                )

    # ======================================
    # VALIDAÇÃO DAS RESTRIÇÕES
    # ======================================

    def validate_restrictions(self):

        restrictions = self.carteira.get(
            "restricoes", {}
        )

        percentage_fields = [
            "volatilidade_maxima",
            "taxa_administrativa_maxima"
        ]

        for name in percentage_fields:

            item = restrictions.get(name)

            if item is None:
                continue

            value = item["value"]

            if 0 <= value <= 100:
                self.results_success(
                    f"Limite '{name}' declarado: {value}%."
                )
            else:
                self.results_error(
                    f"O limite '{name}' deve estar entre 0% e 100%."
                )

        concentration = self.carteira.get(
            "concentracao", {}
        )

        for name, item in concentration.items():

            value = item["value"]

            if item["type"] == "percentage" and 0 <= value <= 100:
                self.results_success(
                    f"Restrição '{name}' declarada: {value}%."
                )
            else:
                self.results_error(
                    f"Restrição '{name}' inválida."
                )

    # ======================================
    # RESULTADOS
    # ======================================

    def results_success(self, message):
        self.resultados.append({
            "status": "SUCESSO",
            "message": message
        })

    def results_error(self, message):
        self.resultados.append({
            "status": "ERRO",
            "message": message
        })

    def show_results(self):

        print("\nRESULTADO DA ANÁLISE")
        print("====================")

        for result in self.resultados:

            print(
                f"[{result['status']}] "
                f"{result['message']}"
            )
