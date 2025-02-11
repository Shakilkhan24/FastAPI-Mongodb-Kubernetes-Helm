import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
    filename='app.log',
    filemode='a'
)

# DEBUG example - detailed information for troubleshooting
def calculate_discount(price, discount_percent):
    logging.debug(f'Starting discount calculation: price={price}, discount={discount_percent}%')
    
    if not isinstance(price, (int, float)) or not isinstance(discount_percent, (int, float)):
        logging.debug(f'Invalid input types: price={type(price)}, discount={type(discount_percent)}')
        return None
    
    discount = price * (discount_percent / 100)
    final_price = price - discount
    
    logging.debug(f'Calculation complete: original={price}, discount={discount}, final={final_price}')
    return final_price

# INFO example - confirm things are working as expected
def process_order(order_id, items):
    logging.info(f'Processing order {order_id} with {len(items)} items')
    
    total = sum(item['price'] for item in items)
    logging.info(f'Order {order_id} processed successfully. Total: ${total}')
    
    return total

# WARNING example - something unexpected but not critical
def check_inventory(product_id, quantity):
    inventory = {
        'A123': 5,
        'B456': 10,
        'C789': 2
    }
    
    available = inventory.get(product_id, 0)
    if available < quantity:
        logging.warning(
            f'Low inventory for product {product_id}. '
            f'Requested: {quantity}, Available: {available}'
        )
    return available >= quantity

# ERROR example - something went wrong that needs attention
def transfer_money(from_account, to_account, amount):
    accounts = {'12345': 1000, '67890': 2000}
    
    try:
        if from_account not in accounts:
            raise ValueError(f"Source account {from_account} not found")
        
        if accounts[from_account] < amount:
            raise ValueError(f"Insufficient funds in account {from_account}")
        
        # Simulate transfer
        logging.info(f"Transferring ${amount} from {from_account} to {to_account}")
        
    except Exception as e:
        logging.error(f"Money transfer failed: {str(e)}", exc_info=True)
        return False
    
    return True

# CRITICAL example - application-breaking issues
def initialize_database():
    try:
        # Simulate database connection
        connected = False
        
        if not connected:
            logging.critical("Failed to connect to database. Application cannot start!")
            raise SystemExit("Database connection failed")
        
    except Exception as e:
        logging.critical(f"Database initialization failed: {str(e)}", exc_info=True)
        raise

# Test all logging levels
def main():
    # Test DEBUG
    print("\nTesting DEBUG logging:")
    calculate_discount(100, 20)
    calculate_discount("invalid", 20)

    # Test INFO
    print("\nTesting INFO logging:")
    process_order("ORD123", [
        {"item": "book", "price": 10},
        {"item": "pen", "price": 5}
    ])

    # Test WARNING
    print("\nTesting WARNING logging:")
    check_inventory("A123", 10)

    # Test ERROR
    print("\nTesting ERROR logging:")
    transfer_money("12345", "67890", 500)  # Should work
    transfer_money("99999", "67890", 500)  # Should fail

    # Test CRITICAL
    print("\nTesting CRITICAL logging:")
    try:
        initialize_database()
    except SystemExit:
        print("Application exit prevented for demonstration")

if __name__ == "__main__":
    main()