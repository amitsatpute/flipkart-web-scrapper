import os
from constant import data_ingestion

class DataIngestionConfig:
        def __init__(self):
            self.data_ingestion_dir: str = os.path.join(
                data_ingestion.ARTIFACT_DIR, data_ingestion.DATA_INGESTION_DIR_NAME
            )

            self.review_store_file_path: str = os.path.join(
                self.data_ingestion_dir, data_ingestion.REVIEW_FILE_NAME
            )

            self.product_list_file_path: str = os.path.join(
                self.data_ingestion_dir, data_ingestion.PRODUCT_LIST_FILE_NAME
            )

