#简单起见直接搞一个自己的日志程序

import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='./data_m/bq.log',
                    level=logging.INFO, format=LOG_FORMAT)


def TMD(niyaoshuosha):
    logging.info(niyaoshuosha)
    print(niyaoshuosha)


def GTMD(niyaoshuosha):
    logging.warning(niyaoshuosha)
    print(niyaoshuosha)


def CTMD(niyaoshuosha):
    logging.error(niyaoshuosha)
    print(niyaoshuosha)

# logging.info("This is a info log.")
# logging.warning("This is a warning log.")
# logging.error("This is a error log.")
# logging.critical("This is a critical log.")
