import argparse
import utils
import traceback
from tqdm import tqdm
from setup_logger import logger
from odcrawler import OpenDataCrawler


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--categories', nargs='+', required=False,
                        help="Categories to save"
                        "(Ex. -c tourism) (default: all)")   # Filtrar por tema
    
    parser.add_argument('-id', '--operation', nargs='+', required=False,
                        help="Operation data to save"
                        "(Ex. -id 61) (default: all)")   # Filtrar por id

    parser.add_argument('-p', '--path', type=str, required=False,
                        help="Path to save data (Ex. -p /my/example/path/)") # Donde ir guardando los archivos


    args = vars(parser.parse_args())

    # Save the arguments into variables
    url = 'https://servicios.ine.es'
    # save_meta = args['save_meta']
    theme = utils.lower_list(args['categories'])
    d_path = args['path']
    o_id = args['operation']
    o_tourism = [61, 62, 63, 132, 180, 238, 239, 240, 241, 328, 329, 330, 334]

    # Show the intro text

    utils.print_intro()

    last_id = None  # Last id save on the file
    save_id = None  # Last id processed
    jump_execution = True
    crawler = None

    try:
        if utils.check_url(url):

            crawler = OpenDataCrawler(url, o_id, o_tourism, theme, d_path)

            # last_id = utils.load_resume_id(crawler.resume_path)

            if crawler.dms:

                # Show info about the number of operations
                logger.info("Obtaining operations from %s", url)
                print("Obtaining operations from " + url)
                operations = crawler.get_operation_list() # Array IDs
                logger.info("%i operations found", len(operations))
                print(str(len(operations)) + " operations found!")

                # if last_id is None or last_id == "":
                #     jump_execution = False

                if operations:
                    # Iterate over each package obtaining the info and saving the dataset
                    for operation_id in tqdm(operations, desc="Processing", colour="green"): # Para cada operacion, obtener todas las tablas

                        # if jump_execution and last_id != operation_id:
                        #     continue
                        # else:
                        #     jump_execution = False

                        tables = crawler.get_tables(operation_id)
                        for table_id in tables:
                            crawler.get_elements(operation_id, table_id)
                            print('Hola')
                            
                        # package = crawler.get_package(id)
                        # if package:

                        #     if args['categories'] and package['theme']:
                        #         exist_cat = any(cat in package['theme'] for cat in categories)
                        #     else:
                        #         exist_cat = True

                        #     resources_save = False
                        #     if len(package['resources']) > 0 and exist_cat:
                        #         for r in package['resources']:
                        #             if(r['downloadUrl'] and r['mediaType'] != ""):
					
                        #                 r['path'] = crawler.save_dataset(r['downloadUrl'], r['mediaType']) # No hace falta
                        #                 if r['path']:
                        #                     resources_save = True
                        #                 save_id = id

                        #         if save_meta and resources_save:
                        #             crawler.save_metadata(package)

                else:
                    print("Error ocurred while obtain packages")

        else:
            print("Incorrect domain form.\nMust have the form "
                "https://domain.example or http://domain.example")

    except Exception as e:

        print(traceback.format_exc())
        print('Keyboard interrumption!')
    finally:
        if save_id:
            utils.save_resume_id(crawler.resume_path, save_id)

    if crawler:
        utils.remove_resume_id(crawler.resume_path)


if __name__ == "__main__":
    main()
