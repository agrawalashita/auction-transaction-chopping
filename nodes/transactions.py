import transactions_generator_usa

NUM_TRANSACTION_TYPES = 6

def transactions_us(num_existing_records):
    transactions = []
    num_transactions_per_type = num_existing_records // NUM_TRANSACTION_TYPES

    execution_start = num_existing_records + 1
    transactions.extend(transactions_generator_usa.generate_t1(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_usa.generate_t2(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_usa.generate_t3(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_usa.generate_t4(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_usa.generate_t5(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_usa.generate_t6(execution_start, execution_start + num_transactions_per_type))

    return transactions

transactions_in = []
transactions_uk = []