import sys
import pytest
sys.path.insert(0, '../')

from src.project import open_file, Operations, Operation, is_supported_card, mask_card, mask_bank

def test_open_file():
    operations_list = open_file('operations.json')
    assert isinstance(operations_list, list)

def test_operations_class():
    operations_manager = Operations()
    assert isinstance(operations_manager, Operations)

def test_operation_class():
    operation = Operation(
        'id', 'state', 'date', 'operation_amount', 'currency_name', 'currency_code', 'description', 'from_', 'to_'
    )
    assert isinstance(operation, Operation)

def test_is_supported_card():
    assert is_supported_card('VISA') is True
    assert is_supported_card('MASTERCARD') is True
    assert is_supported_card('MAESTRO') is True
    assert is_supported_card('Unsupported Card') is False

def test_mask_card():
    transaction_info = ['MAESTRO', '1234567890123456']
    assert mask_card(transaction_info) == 'MAESTRO 1234 56** **** 3456'

def test_mask_bank():
    transaction_info = ['Счет', '1234567890123456']
    assert mask_bank(transaction_info) == 'Счет **3456'

def test_operations_manager_add_operation():
    operations_manager = Operations()
    operation = Operation(
        'id', 'state', 'date', 'operation_amount', 'currency_name', 'currency_code', 'description', 'from_', 'to_'
    )
    operations_manager.add_operation(operation)
    assert len(operations_manager.operations) == 1

def test_sorting_by_date():
    """Test that sorting operations by date works."""
    operations_manager = Operations()
    operations = [
        Operation(
            'id1', 'state', '13.11.2019', 'operation_amount', 'currency_name', 'currency_code', 'description', 'from_', 'to_'
        ),
        Operation(
            'id2', 'state', '13.12.2019', 'operation_amount', 'currency_name', 'currency_code', 'description', 'from_', 'to_'
        ),
    ]
    for operation in operations:
        operations_manager.add_operation(operation)

    operations_manager.sort_operations_by_date()

    assert operations_manager.operations[0].date > operations_manager.operations[1].date

def test_operations_manager_print_last_5_operations(capsys):
    operations_manager = Operations()
    operation1 = Operation(
        'id1', 'state', '01.01.2022', 'operation_amount', 'currency_name', 'currency_code', 'description', 'Maestro 1234567890123456', 'Maestro 1234567890123456'
    )
    operation2 = Operation(
        'id2', 'state', '02.01.2022', 'operation_amount', 'currency_name', 'currency_code', 'description', 'Maestro 1234567890123456', 'Maestro 1234567890123456'
    )
    operation3 = Operation(
        'id3', 'state', '03.01.2022', 'operation_amount', 'currency_name', 'currency_code', 'description', 'Maestro 1234567890123456', 'Maestro 1234567890123456'
    )
    operation4 = Operation(
        'id4', 'state', '04.01.2022', 'operation_amount', 'currency_name', 'currency_code', 'description', 'Maestro 1234567890123456', 'Maestro 1234567890123456'
    )
    operation5 = Operation(
        'id5', 'state', '05.01.2022', 'operation_amount', 'currency_name', 'currency_code', 'description', 'Maestro 1234567890123456', 'Maestro 1234567890123456'
    )
    operations_manager.add_operation(operation1)
    operations_manager.add_operation(operation2)
    operations_manager.add_operation(operation3)
    operations_manager.add_operation(operation4)
    operations_manager.add_operation(operation5)
    operations_manager.sort_operations_by_date()
    operations_manager.print_last_5_operations()
    assert operations_manager.operations == [operation5, operation4, operation3, operation2, operation1]
    assert len(operations_manager.operations) == 5
    
if __name__ == '__main__':
    pytest.main()