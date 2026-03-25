from .logHelper import AppLogger

def mark_start_of_execution(file_path):
    with open(file_path, "a") as file:
        file.write("\n\n" + "*" * 10 + " New Execution " + "*" * 10 + "\n\n")


def write_latency_summary(file_path, data):

    logger = AppLogger.getInstance(file_path)
    # logger.info('JOnaed')
    logger.info("*" * 30 + " Latency Summary " + "*" * 30 + "\n")

    for key, value in data.items():
        if key == "total_calls":
            logger.info(f"{key}: {value}\n")
        else:
            logger.info(f"{key}: {value} seconds\n")
    logger.info("*" * 30 + " End Latency Summary " + "*" * 27 + "\n\n")
