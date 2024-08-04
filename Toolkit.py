import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#################
# 存檔
#################         
def save_to_file(filename: str, content, mode: str = 'w') -> bool:
    if not isinstance(content, str):
        logging.error("Content must be a string")
        return False
    try:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
            logging.info(f"Directory created or already exists: {directory}")
        
        with open(filename, mode, encoding='utf-8') as file:
            file.write(content)
        logging.info(f"Successfully saved to {filename}")
        return True
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except IOError as e:
        logging.error(f"IO error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    
    return False




def read_file_to_list(filename):
  """
  將檔案讀取為一個 list，每一行為一個元素

  Args:
    filename: 檔案名稱

  Returns:
    一個包含檔案內容的 list
  """

  with open(filename, 'r') as f:
    lines = f.readlines()
  lines = [line.rstrip() for line in lines]
  return lines
