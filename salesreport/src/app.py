# app.py

from src import access_database as ad
import os
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Configure logging
# Create the "log" folder
output_folder = 'log'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
logging.basicConfig(filename=f'{output_folder}/audit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Sales:
    # initialization of variables
    def __init__(self):
        self.sales_data = pd.DataFrame()
        self.total_prices_per_product = {}
        self.total_prices_per_year = {}
        self.average_prices = {}
        self.sales_distribution = {}

    # get sales info from csv and update to db
    def get_sales_data(self, csv_file='src/input/sales_data.csv'):  # Updated file path
        try:
            logging.info(
                "Initiating the process of sales data from csv file to store in the database.")
            self.sales_data = pd.read_csv(csv_file).dropna()
            ad.set_data_to_db(self.sales_data.to_dict(orient='records'))
        except FileNotFoundError:
            logging.error("Error: sales_data.csv file not found.")
        except Exception as e:
            logging.error(
                "An error occurred while getting sales data: %s", str(e))

    # create a data set from database to generate graphs
    def generic_product_set(self, table_prefix='', table_name ='salestable'):
        try:
            product_set = ad.retrieve_info_from_table(
                'sales', f"{table_prefix}{table_name}")
            for name, price, quantity, year in [(item[0], item[1], item[2], pd.to_datetime(str(item[3])).year) for item in product_set]:
                total = price * quantity
                self.total_prices_per_product[name] = self.total_prices_per_product.get(
                    name, 0) + total
                self.total_prices_per_year[year] = self.total_prices_per_year.get(
                    year, 0) + total
                self.sales_distribution[name] = self.sales_distribution.get(
                    name, []) + [quantity]
            self.sales_distribution = {
                name: sum(quantities) for name, quantities in self.sales_distribution.items()}
            self.average_prices = {
                name: self.total_prices_per_product[name] / self.sales_distribution[name] for name in self.total_prices_per_product}
            logging.info("Sales processed data set created succesfully.")
            self.drawPlotChart()
        except Exception as e:
            logging.error(
                "An error occurred while generating the data set: " + str(e))

    # draw plot charts for each data
    def drawPlotChart(self):
        # Create the "output" folder
        output_folder = 'output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        try:
            logging.info("Initiated process to generate sales report")
            pdf_file = f'{output_folder}/sales_report.pdf'
            pdf_pages = PdfPages(pdf_file)
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            plots = [
                (self.total_prices_per_product, 'Product', 'Total sales',
                 'Total Sales per Product', 'blue'),
                (self.total_prices_per_year, 'Year',
                 'Total sales', 'Total Sales per Year', 'green'),
                (self.average_prices, 'Product', 'Total Average Prices',
                 'Average Price per Product', 'red'),
                (self.sales_distribution, 'Product', 'Quantity',
                 'Sales Distribution by Quantity', 'orange')
            ]
            for i, (data, x_label, y_label, title, color) in enumerate(plots):
                ax = axes[i // 2, i % 2]
                plot_data = pd.DataFrame(
                    {x_label: data.keys(), y_label: data.values()})
                plot_data.plot.line(x=x_label, y=y_label,
                                    rot=90, color=color, ax=ax)
                ax.set_ylabel(y_label)
                ax.set_xlabel(x_label)
                ax.set_title(title)
            plt.tight_layout()
            pdf_pages.savefig(fig)
            pdf_pages.close()
            logging.info("Successfully generated sales report as pdf")
        except Exception as e:
            logging.error(
                "An error occurred while drawing plot charts:", str(e))

    # store processed information to db by creating tables
    def set_processed_info_to_db(self, dbname='total_sales', table_prefix=''):
        try:
            logging.info(
                "Initiated the process of storing the processed data to db")
            data_to_store = {
                'products': self.total_prices_per_product,
                'years': self.total_prices_per_year,
                'average': self.average_prices,
                'quantity': self.sales_distribution
            }
            for table_name, data in data_to_store.items():
                ad.set_processed_data_to_db(
                    dbname, f"{table_prefix}{table_name}", data)
        except Exception as e:
            logging.error(
                "An error occurred while intiating of storing processed data:", str(e))

    # retrieve the processed info from table if required (testing purpose)
    def retrieve_info_from_table_data(self, dbname='total_sales', table_prefix=''):
        try:
            logging.info(
                "Successfully initiated the process of retrieving information")
            tables_to_retrieve = ['products', 'years', 'average', 'quantity']
            for table_name in tables_to_retrieve:
                ad.retrieve_info_from_table(
                    dbname, f"{table_prefix}{table_name}")
        except Exception as e:
            logging.error("An error occurred while the process of initiating retrieving information from the table:",
                          str(e))
