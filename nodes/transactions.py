import nodes.transactions_generator_in as transactions_generator_in
import nodes.transactions_generator_usa as transactions_generator_usa

NUM_TRANSACTION_TYPES = 6

# Define global ID ranges for each region
USA_RANGE = (1, 10000)
INDIA_RANGE = (10001, 20000)
UK_RANGE = (20001, 30000)

def transactions_us(num_existing_records):
    transactions = []
    num_transactions_per_type = num_existing_records // NUM_TRANSACTION_TYPES

    execution_start = num_existing_records + USA_RANGE[0]
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

def transactions_in(num_existing_records):
    transactions = []
    num_transactions_per_type = num_existing_records // NUM_TRANSACTION_TYPES

    execution_start = num_existing_records + INDIA_RANGE[0]
    transactions.extend(transactions_generator_in.generate_t1(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_in.generate_t2(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_in.generate_t3(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_in.generate_t4(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_in.generate_t5(execution_start, execution_start + num_transactions_per_type))

    execution_start = execution_start + num_transactions_per_type
    transactions.extend(transactions_generator_in.generate_t6(execution_start, execution_start + num_transactions_per_type))

    return transactions