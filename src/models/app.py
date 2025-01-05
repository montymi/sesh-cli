import configparser
import os
import logging

class App:
    def __init__(self):
        self.PROJECT_DIR = os.path.dirname(os.getcwd())
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logger()
        self.load_config()
        self.check_paths()
 
    def load_config(self):
        # Initialize and read the configuration file
        self.config.read(os.path.join(self.PROJECT_DIR, 'config.ini'))

        # Accessing settings
        self.DEBUG = self.config.getboolean('settings', 'debug')
        self.CLERK = self.config.get('settings', 'clerk')
        self.LIBRARIAN = self.config.get('settings', 'librarian')
        self.LLM = self.config.get('settings', 'llm')

        # Accessing library file settings
        self.FILE_DATA_DIRECTORY = os.path.join(self.PROJECT_DIR, self.config['library.file'].get('data', ''))

        # Accessing library mongo settings
        self.MONGO_URL = self.config['library.mongo'].get('url', '')
        self.MONGO_USERNAME = self.config['library.mongo'].get('username', '')
        self.MONGO_PASSWORD = self.config['library.mongo'].get('password', '')
        self.check_paths()
        
        self.OPENAI_API = self.config['keys'].get('openai', '')

    def setup_logger(self):
        # Set up the logger
        self.logger.setLevel(logging.DEBUG)  # Set the logging level
        
        # Create file handler for logging
        log_file = os.path.join(self.PROJECT_DIR, 'sesh.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler for logging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


    def check_paths(self):
        # Ensure that the file data directory exists, create it if not
        if not os.path.exists(self.FILE_DATA_DIRECTORY):
            os.makedirs(self.FILE_DATA_DIRECTORY)
            self.logger.info(f"Created data directory: {self.FILE_DATA_DIRECTORY}")

    def get_config(self):
        return self.config

    def get_mongo_credentials(self):
        return {
            'url': self.MONGO_URL,
            'username': self.MONGO_USERNAME,
            'password': self.MONGO_PASSWORD
        }
