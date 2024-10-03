from os import getenv
from typing import Optional
from pandas import DataFrame
from pymongo import MongoClient
from dotenv import load_dotenv
from certifi import where
from MonsterLab.monster_lab import Monster

load_dotenv()
client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
db = client["BandersnatchDB"]

class Database:

    def __init__(self, collection_name: str):
        """
        Initializes the Database instance by connecting to the specified collection.

        Parameters:
        - collection_name (str): The name of the collection to interact with.
        """
        load_dotenv()
        db_url = getenv("DB_URL")
        if not db_url:
            raise ValueError("Database URL not found in environment variables.")
        self.client = MongoClient(db_url, tlsCAFile=where())
        self.db = self.client["BandersnatchDB"]
        self.collection = self.db[collection_name]

    def seed(self, n:int) -> None:
        """
        Inserts 'n' random monster documents into the collection.

        Parameters:
        - n (int): Number of monster documents to insert.
        """

        try:
            monsters = [Monster().to_dict() for _ in range(n)]
            if monsters:
                result = self.collection.insert_many(monsters)
                print(f"Inserted {len(result.inserted_ids)} documents into the collection.")
        except Exception as e:
            print(f"An error occurred during seeding: {e}")

    def reset(self) -> None:
        """
        Deletes all documents from the collection.
        """
        self.collection.delete_many({})

    def count(self) -> int:
        """
        Returns the number of documents in the collection.

        Returns:
        - int: The count of documents.
        """
        return self.collection.count_documents({})

    def dataframe(self) -> Optional[DataFrame]:
        """
        Retrieves all documents from the collection as a pandas DataFrame.

        Returns:
        - DataFrame: The DataFrame containing all documents.
        - None: If the collection is empty.
        """
        data = list(self.collection.find({}, {'_id': False}))
        if data:
            return DataFrame(data)
        else:
            return None

    def html_table(self) -> str:
        """
        Returns an HTML table representation of the DataFrame.

        Returns:
        - str: An HTML table as a string.
        - None: If the collection is empty.
        """
        df = self.dataframe()
        if df is not None:
            return df.to_html(index=False)
        else:
            return None


