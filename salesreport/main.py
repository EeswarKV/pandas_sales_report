# main.py

from src.app import Sales

if __name__ == '__main__':
    sales_info = Sales()
    sales_info.get_sales_data()
    sales_info.generic_product_set()
    sales_info.set_processed_info_to_db()
    sales_info.retrieve_info_from_table_data()
