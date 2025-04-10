import os
from dotenv import load_dotenv

from hh import get_statistic as get_hh_statistic  
from sj import get_statistic as get_sj_statistic
from helper import get_table


if __name__ == '__main__':
    load_dotenv()
    secret_key = os.environ['SUPERJOB_SECRET_KEY']
    sj_statistic = get_sj_statistic(secret_key)
    print(get_table('SuperJob', statistic=sj_statistic))
    
    hh_statistic = get_hh_statistic()
    print(get_table('HeadHunter', statistic=hh_statistic))