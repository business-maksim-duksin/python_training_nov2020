def get_logger(logger_name, logs_filename="logs"):
    import logging
    import os

    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    dirname = "logs"
    filename = f"{logs_filename}.log"
    log_folder = os.path.join(os.getcwd(), dirname)
    log_pathname = os.path.join(os.getcwd(), dirname, filename)
    os.makedirs(log_folder, exist_ok=True)
    log_file = logging.FileHandler(log_pathname)
    log_console = logging.StreamHandler()
    log_console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(filename)s %(funcName)s %(message)s")
    log_file.setFormatter(formatter)
    log_console.setFormatter(formatter)
    log.addHandler(log_file)
    log.addHandler(log_console)
    return log
