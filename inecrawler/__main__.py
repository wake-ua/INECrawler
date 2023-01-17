import argparse
import utils
from tqdm import tqdm
from setup_logger import logger
import traceback


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--domain', type=str,
                        help='A data source (Ex. -d https://domain.example)', # Ignorar
                        required=True)

    parser.add_argument('-m', '--save_meta', required=False,
                        action=argparse.BooleanOptionalAction,
                        help='Save dataset metadata (default: not save)')   # Ignorar

    parser.add_argument('-t', '--data_types', nargs='+', required=False,
                        help="data types to save (Ex. -t xls pdf)"          # Siempre csv
                        "(default: all)")

    parser.add_argument('-c', '--categories', nargs='+', required=False,
                        help="Categories to save"
                        "(Ex. -c crime tourism transport) (default: all)")   # Filtrar por id

    parser.add_argument('-p', '--path', type=str, required=False,
                        help="Path to save data (Ex. -p /my/example/path/)") # Donde ir guardando los archivos

    parser.add_argument('-s', '--max_seconds', type=int, required=False,
                        help="Max seconds employed downloading a file (Ex. -s 60)") # Ignorar

    args = vars(parser.parse_args())

    # Save the arguments into variables
    url = args['domain']
    d_types = args['data_types']
    save_meta = args['save_meta']
    categories = utils.lower_list(args['categories'])
    d_path = args['path']
    max_sec = args['max_seconds']

    # Show the intro text

    utils.print_intro()

    last_id = None  # Last id save on the file
    save_id = None  # Last id processed
    jump_execution = True
    crawler = None

    try:
        if utils.check_url(url):

            # crawler = OpenDataCrawler(url, path=d_path, data_types=d_types, sec=max_sec)

            last_id = utils.load_resume_id(crawler.resume_path)

            if crawler.dms:

                # Show info about the number of packages
                logger.info("Obtaining packages from %s", url)
                print("Obtaining packages from " + url)
                packages = crawler.get_package_list() # Array IDs
                logger.info("%i packages found", len(packages))
                print(str(len(packages)) + " packages found!")

                if last_id is None or last_id == "":
                    jump_execution = False

                if packages:
                    # Iterate over each package obtaining the info and saving the dataset
                    for id in tqdm(packages, desc="Processing", colour="green"): # Para cada operacion, obtener todas las tablas

                        if jump_execution and last_id != id:
                            continue
                        else:
                            jump_execution = False

                        package = crawler.get_package(id)

                        if package:

                            if args['categories'] and package['theme']:
                                exist_cat = any(cat in package['theme'] for cat in categories)
                            else:
                                exist_cat = True

                            resources_save = False
                            if len(package['resources']) > 0 and exist_cat:
                                for r in package['resources']:
                                    if(r['downloadUrl'] and r['mediaType'] != ""):
					
                                        r['path'] = crawler.save_dataset(r['downloadUrl'], r['mediaType']) # No hace falta
                                        if r['path']:
                                            resources_save = True
                                        save_id = id

                                if save_meta and resources_save:
                                    crawler.save_metadata(package)

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
