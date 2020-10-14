import sys


class Calculator:
    def __init__(self):
        self.calc_on = True
        self.user_variables = {}
        self.last_answer = None
        self.user_input = None
        self.result_list = list()
        self.precedence = {'+': 0,  # Utilizado para determinar a ordem de operações.
                           '-': 0,  # Um número maior indica maior preferência de operação.
                           '*': 1,
                           '/': 1,
                           }

    def get_input(self):
        if self.calc_on:
            self.result_list = list()
            self.user_input = list(input())
            while ' ' in self.user_input:
                self.user_input.remove(' ')
            self.input_parsing(self.user_input)
        else:
            sys.exit()

    def input_parsing(self, input_list):
        if len(input_list) != 0:
            if input_list[0] == '/':
                execute_command(''.join(input_list))
                self.get_input()
            else:
                try:
                    print(int(''.join(input_list)))
                    self.get_input()
                except ValueError:
                    pass
            if '=' in input_list:
                self.declare_variable(input_list)
            elif '+' in input_list or '-' in input_list or '/' in input_list or '*' in input_list:
                self.infix_to_postfix(input_list)
            elif ''.join(input_list).isalpha():
                print(self.user_variables.get(''.join(input_list), 'Unknown variable'))
        self.get_input()

    def declare_variable(self, input_list):
        # Esse bloquinho toma conta da entrada de tal modo que o usuário pode declarar variáveis de qualquer forma.

        # Primeiro testamos se o usuário não escreveu algo com vários sinais '=' (x == 3 ou x = 3 = 4)
        if input_list.count('=') > 1:
            print('Invalid assignment')
            return

        # Caso o usuário escreva corretamente, dividiremos a lista em duas partes. Uma antes do '=' e outra depois:
        # Input_list deve ficar assim: ['nome da variável', 'valor a ser atribuído']
        input_list = ''.join(input_list).split('=')

        # Aqui testamos as várias condições pedidas pela tarefa
        # Não aceitamos variáveis com número (a3 = 4)
        if not input_list[0].isalpha():
            print('Invalid identifier')
            return

        # No caso do usuário querer declarar 'x = a' onde 'a' pode ser uma variável já existente com um valor.
        # E também, se 'a' não existe, avisamos o usuário.
        if input_list[1].isalpha() and input_list[1] in self.user_variables:
            self.user_variables[input_list[0]] = self.user_variables[input_list[1]]
        elif input_list[1].isalpha() and input_list[1] not in self.user_variables:
            print('Unknown variable')
        elif not input_list[1].isalpha() and not input_list[1].isdecimal():  # Verificando se 'a' é uma entrada válida
            print('Invalid assignment')  # (contém somente letras).
        elif input_list[1].isdecimal():  # Por último, o caso mais básico 'x = 4' ('letra' = 'número')
            self.user_variables[input_list[0]] = int(input_list[1])

    def sign_parse(self, number_list):
        for i in range(len(number_list) - 2):
            try:
                while number_list[i + 1].isdecimal() and number_list[i].isdecimal():  # Corrigindo a situação '1' '2' ->'12'
                    number_list[i] += number_list[i + 1]
                    number_list.remove(number_list[i + 1])
                while number_list[i + 1] in self.precedence and number_list[i] in self.precedence:
                    if self.precedence[number_list[i]] != 0:
                        print('Invalid expression')
                        self.get_input()
                    elif number_list[i] == number_list[i + 1] and self.precedence[number_list[i]] == 0:
                        number_list[i] = '+'
                        number_list.remove(number_list[i + 1])
                    else:
                        number_list[i] = '-'
                        number_list.remove(number_list[i + 1])
            except IndexError:
                break
        return number_list

    def infix_to_postfix(self, number_list):
        operator_stk = list()
        parsed_number_list = self.sign_parse(number_list)

        for element in parsed_number_list:

            #            for character in element:

            # 1- Se o character é um número ou letra, ela vai para o result_list
            if element.isdecimal() or element.isalpha():
                self.result_list.append(element)

            # Se o character é um operador:
            # 2- Se o operator_stk está vazio ou contém um "(" no topo, o character vai para o topo
            elif len(operator_stk) == 0 or operator_stk[-1] == '(':
                operator_stk.append(element)

            # 5- Se o character é um "(" ele vai para o topo do operator_stk
            elif element == '(':
                operator_stk.append(element)

            # 6- Se o character é um ")", operator_stk.pop até o topo ser "(". Descartar ambos os parentesis
            elif element == ')':
                try:
                    while operator_stk[-1] != '(':
                        self.result_list.append(operator_stk.pop())
                    operator_stk.pop()
                except IndexError:
                    print('Invalid expression')
                    self.get_input()

            # 3- Se o character possui maior prioridade que o topo do operator_stk, o charactere vai para o topo
            elif self.precedence[element] > self.precedence[operator_stk[-1]]:
                operator_stk.append(element)

            # 4- Se o character tem prioridade menor ou igual que o topo do operator_stk
            # realiza-se operator_stk pop e os operadores são colocados no result_list
            # até que o topo do operator_stk tenha menor prioridade ou seja um "("
            elif self.precedence[element] <= self.precedence[operator_stk[-1]]:
                while len(operator_stk) != 0 \
                        and (operator_stk[-1] != '('
                             or self.precedence.get(element, -1) <= self.precedence.get(operator_stk[-1], -1)):
                    self.result_list.append(operator_stk.pop())
                operator_stk.append(element)
        while len(operator_stk) != 0:
            if operator_stk[-1] == "(":
                print('Invalid expression')
                self.get_input()
            else:
                self.result_list.append(operator_stk.pop())
        self.calculate_result(self.result_list)

    def calculate_result(self, result_list):
        temp_result_stack = list()
        for element in result_list:
            if element.isdecimal():
                temp_result_stack.append(element)
            elif element.isalpha():
                try:
                    temp_result_stack.append(self.user_variables[element])
                except KeyError:
                    print('Unknown variable')
            elif element in self.precedence:
                operand2 = temp_result_stack.pop()
                operand1 = temp_result_stack.pop()
                temp_result_stack.append(single_operation(element, operand1, operand2))
        print(temp_result_stack.pop())
        self.get_input()


def single_operation(operator, operand1, operand2):  # Switch para as operações da calculadora
    operation = {  # todo: adicionar potênciacão
        '+': str(int(operand1) + int(operand2)),
        '-': str(int(operand1) - int(operand2)),
        '*': str(int(operand1) * int(operand2)),
        '/': str(int(int(operand1) / int(operand2)))
    }
    return operation.get(operator, 'Invalid operator')


def calc_exit():
    program.calc_on = False
    return print('Bye!')


def calc_help():
    return print('This program is a calculator that can assign variables using "=" sign and make operations using: "+" '
                 ', "-", "*" and "/"')


def calc_vars():
    return print(program.user_variables)


def execute_command(command_str):  # Switch para os comandos da calculadora
    commands = {
        '/exit': calc_exit,
        '/help': calc_help,
        '/vars': calc_vars
    }
    command = commands.get(command_str)
    if command is None:
        return print('Unknown command')
    return command()


program = Calculator()
while program.calc_on:
    program.get_input()
