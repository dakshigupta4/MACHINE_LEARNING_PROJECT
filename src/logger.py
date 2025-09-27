import logging  #record events(info,warning,errors)
import os   #handling path an folder
from datetime import datetime
LOG_FILE=f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"  #log file name with date and time
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) #logs folder path,get current working directory.
os.makedirs(logs_path,exist_ok=True)
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    # %(name)s → Logger name (by default, "root")
    # %(levelname)s → Type of log (INFO, ERROR, WARNING, CRITICAL)
)
# if __name__=="__main__":
#     logging.info("Logging has started")