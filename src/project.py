from datetime import datetime
import json, os

def open_file(filename):
    """
    Загружает json файл operations.
    
    Возвращает список словарей с информацией о транзакциях.
    """
    current_directory = os.path.dirname(__file__)
    path = os.path.join(current_directory, 'operations.json')
    with open(path, 'r', encoding='utf-8') as file:
        operations_info = json.load(file)
    return operations_info

def print_transaction(obj):
    """
    Выводит информацию о транзакции в нужном формате.
    """
    # Разделяем строку from_ на отдельные слова
    splitted_str_from = obj.from_.split(" ")
    
    # Разделяем строку to_ на отдельные слова
    splitted_str_to = obj.to_.split(" ")
    
    # Если from_ - это счет, то готовим текст для счета
    if splitted_str_from[0] == 'Счет':
        from_text = mask_bank(splitted_str_from)
    
    # Если from_ - это карта, то готовим текст для карты
    if is_supported_card(splitted_str_from[0]):
        from_text = mask_card(splitted_str_from)
    
    # Если to_ - это счет, то готовим текст для счета
    if splitted_str_to[0] == 'Счет':
        to_text = mask_bank(splitted_str_to)
    
    # Если to_ - это карта, то готовим текст для карты
    if is_supported_card(splitted_str_to[0]):
        to_text = mask_card(splitted_str_to)
    
    # Выводим информацию о транзакции
    print(from_text, '->', to_text)


def is_supported_card(card_type):
    """
    Проверяет наличие поддерживаемых типов карт.
    
    Поддерживаемые типы карт: VISA, MASTERCARD, MAESTRO.
    """
    supported_cards = {"VISA", "MASTERCARD", "MAESTRO"} 
    return card_type.upper() in supported_cards

def mask_card(transaction_info):
    """
    Метод маскирует номер карты, оставляя только
    первые 4 и последние 4 цифры.
    """
    if transaction_info[1].isdigit():
        return f"{transaction_info[0]} {transaction_info[1][0:4]} {transaction_info[1][4:6]}** **** {transaction_info[1][-4:]}"
    else:
        return f"{transaction_info[0]} {transaction_info[1]} {transaction_info[2][0:4]} {transaction_info[2][4:6]}** **** {transaction_info[2][-4:]}"

def mask_bank(transaction_info):
    """
    Метод маскирует информацию о банковском счете, оставляя 
    только 4 последние цифры.
    """
    return f"{transaction_info[0]} **{transaction_info[1][-4:]}"

class Operations():
    """
    Класс, содержащий список из операций.
    Список содержит словари с информацией о транзакциях.
    Сортирует список по дате.
    Выводит последние 5 операций.
    """
    def __init__(self):
        self.operations = []

    def add_operation(self, operation):
        self.operations.append(operation)
     
    def sort_operations_by_date(self):
        """
        Метод сортирует список операций по дате.
        В результате списка операций будет отсортирован по дате,
        начиная с последней операции.
        """
    def sort_operations_by_date(self):
        def convert_date_to_string(operation):
            original_date = operation.date
            date_format = "%d.%m.%Y"
            return datetime.strptime(original_date, date_format).strftime("%Y-%m-%d")
        self.operations = sorted(self.operations, key=convert_date_to_string, reverse = True)
    
    def print_last_5_operations(self):
        five_last_operations = self.operations[0:5]
        for obj in five_last_operations:
            print(f"{obj.date} {obj.description}")
            try:
                print_transaction(obj)
            except AttributeError:
                splitted_str_to = obj.to_.split(" ")
                print(f"{splitted_str_to[0]} **{splitted_str_to[1][-4:]}")
            print(f"{obj.operation_amount} {obj.currency_name}\n")

class Operation:
    """
    Класс, содержащий информацию о транзакции.
    Поля: id, state, date, operation_amount, currency_name, currency_code, description, from_, to_.
    """
    def __init__(self, id, state, date, operation_amount, currency_name, currency_code, description, from_, to_):
        self.id = id
        self.state = state
        self.date = date
        self.operation_amount = operation_amount
        self.currency_name = currency_name
        self.currency_code = currency_code
        self.description = description
        self.from_ = from_
        self.to_ = to_

Operations_manager = Operations() #Создаем список операций.

operations_list = open_file('operations.json') #Загружаем файл operations.json
for item in operations_list: #Пропускаем отклоненные операции.
    if item['state'] == 'CANCELED':
        continue
    try: #Создаем класс операции.
        obj = Operation(    
            item['id'],
            item['state'],
            datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime("%d.%m.%Y"),
            item['operationAmount']['amount'],
            item['operationAmount']['currency']['name'],
            item['operationAmount']['currency']['code'],
            item['description'],
            item.get('from'),
            item['to']
        )
    except KeyError as e: #Выводим ошибку при отсутствии ключа.
        print(f"Missing key: {e}")
    Operations_manager.add_operation(obj) #Добавляем операцию в список.
    
Operations_manager.sort_operations_by_date() #Сортируем список по дате.
Operations_manager.print_last_5_operations() #Выводим последние 5 операций.

if '13.11.2019' < '13.12.2019':
    print('True')
else:
    print('False')
# Пример вывода для одной операции:
#14.10.2018 Перевод организации
#Visa Platinum 7000 79** **** 6361 -> Счет **9638
#82771.72 руб.


