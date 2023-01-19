import argparse
import utils
import traceback
import pandas as pd
from tqdm import tqdm
from setup_logger import logger
from odcrawler import OpenDataCrawler


def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-m', '--save_meta', required=False,
                        action=argparse.BooleanOptionalAction,
                        help='Save dataset metadata (default: not save)')

    parser.add_argument('-c', '--categories', nargs='+', required=False,
                        help="Categories to save"
                        "(Ex. -c tourism) (default: all)")   # Filtrar por tema
    
    parser.add_argument('-y', '--year', type=str, required=False,
                        help="Operation data from this year to save"
                        "(Ex. -y 2020) (default: all)")   # Filtrar por anyo
    
    parser.add_argument('-id', '--operation', type=str, required=False,
                        help="Operation data to save"
                        "(Ex. -id 61) (default: all)")   # Filtrar por id

    parser.add_argument('-p', '--path', type=str, required=False,
                        help="Path to save data (Ex. -p /my/example/path/)") # Donde ir guardando los archivos


    args = vars(parser.parse_args())

    # Save the arguments into variables
    url = 'https://servicios.ine.es'
    save_meta = args['save_meta']
    categories = utils.lower_list(args['categories'])
    d_path = args['path']
    o_id = args['operation']
    year = args['year']
    o_tourism = [61, 62, 63, 132, 180, 238, 239, 240, 241, 328, 329, 330, 334]

    # Show the intro text

    utils.print_intro()

    save_id = None  # Last id processed
    crawler = None

    try:
        if utils.check_url(url):

            crawler = OpenDataCrawler(url, o_id, o_tourism, categories, year, d_path)

            # last_id = utils.load_resume_id(crawler.resume_path)

            if crawler.dms:

                # Show info about the number of operations
                logger.info("Obtaining operations from %s", url)
                print("Obtaining operations from " + url)
                
                if o_id:
                    operations = []
                    operations.append(int(o_id))
                else:
                    operations = crawler.get_operation_list() # Array IDs
                
                logger.info("%i operations found", len(operations))
                print(str(len(operations)) + " operations found!")

                if operations:
                    # Iterate over each package obtaining the info and saving the dataset
                    for operation_id in tqdm(operations, desc="Processing", colour="green"): # Para cada operacion, obtener todas las tablas

                        tables = crawler.get_tables(operation_id)
                        for x in tables:
                            for x in crawler.get_tables(operation_id):
                                elements = crawler.get_elements(operation_id, x)
                                
                                if elements:
                                    crawler.save_metadata(elements)
                                    crawler.save_dataset(elements)
                else:
                    print("Error ocurred while obtain packages")

        else:
            print("Incorrect domain form.\nMust have the form "
                "https://domain.example or http://domain.example")

    except Exception as e:

        print(traceback.format_exc())
        print('Keyboard interrumption!')

    if crawler:
        utils.remove_resume_id(crawler.resume_path)


if __name__ == "__main__":
    main()
