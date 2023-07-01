# test_app.py

import pytest
from main import Sales
import pandas as pd


@pytest.fixture
def sales_info():
    return Sales()


def test_get_sales_data(sales_info):
    sales_info.get_sales_data('salesreport/src/input/sales_data.csv')
    assert len(sales_info.sales_data) > 0


def test_generic_product_set(sales_info):
    sales_info.sales_data = pd.DataFrame({
        'product_name': ['Product 1', 'Product 2'],
        'quantity_sold': [10, 5],
        'price': [5.99, 9.99],
        'date_of_sale': ['2023-06-28', '2023-06-29']
    })
    sales_info.generic_product_set()
    assert len(sales_info.total_prices_per_product) > 0
    assert len(sales_info.total_prices_per_year) > 0
    assert len(sales_info.average_prices) > 0
    assert len(sales_info.sales_distribution) > 0


def test_set_processed_info_to_db(sales_info):
    sales_info.sales_data = pd.DataFrame({
        'product_name': ['Product 1', 'Product 2'],
        'quantity_sold': [10, 5],
        'price': [5.99, 9.99],
        'date_of_sale': ['2023-06-28', '2023-06-29']
    })
    sales_info.generic_product_set()
    sales_info.set_processed_info_to_db(
        dbname='test_sales', table_prefix='test_')

    # You can add assertions to check if the data is stored in the database


def test_retrieve_info_from_table_data(sales_info):
    sales_info.retrieve_info_from_table_data(
        dbname='test_sales', table_prefix='test_')

    # You can add assertions to check the retrieved data from the tables if needed


# Run the tests
if __name__ == "__main__":
    pytest.main()
