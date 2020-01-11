import argparse
from m_acquisition import module_acquire
from m_wrangling import module_wrangling
from m_analysis import module_analysis
from m_reporting import module_reporting

def main(file_name):
    path = './data/raw/herreradelduque.db'
    #file_name = 'Forbes_data_analisys_2018'
    print('\n--- WELCOME TO THE FORBES HACK-REPORTING ---\n')
    forbes_df = module_acquire.acquisition(path)
    module_acquire.save_table(forbes_df,'forbes_df')
    df_forbes_kag = module_acquire.api_kaggle()
    df_forbes_country = module_wrangling.wrangling('df_forbes_kag')
    module_analysis.plot(df_forbes_country)
    module_reporting.create_ppt(file_name)
    module_reporting.send_email(file_name)
    print('\nPlease, remember that you PPT report is located at: ./data/results')
    print('\n--- THANKS FOR USE FORBES ---\n       HACK-REPORTING')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_name", help = "The name of the PowerPoint reported", dest='file_name', default='Forbes_Data_Analysis_2018')
    args = parser.parse_args()
    file_name = args.file_name
    main(file_name)