from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from .generic_crud import GenericCRUD
from .utils import validate_none_select_table_name


# Load environment variables
load_dotenv()

# Constants
DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_ID = 206
DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_NAME = 'circles_local_database_python\\generic_mapping'
DEVELOPER_EMAIL = 'sahar.g@circ.zone'

# Logger setup
logger = Logger.create_logger(object={
    'component_id': DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_ID,
    'component_name': DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
})


class GenericMapping(GenericCRUD):

    def __init__(self, default_schema_name: str = None, default_table_name: str = None, default_linked_table_name: str = None):
        super().__init__(default_schema_name=default_schema_name,
                         default_table_name=default_table_name)
        self.default_schema_name = default_schema_name
        self.default_table_name = default_table_name
        self.default_linked_table_name = default_linked_table_name

    def insert_link(self, table_name: str, linked_table_name: str, entity_id1: int, entity_id2: int) -> int:
        """Inserts a new link between two entities and returns the id of the new row or -1 if an error occurred.
        :param table_name: The name of the first entity's table.
        :param linked_table_name: The name of the second entity's table.
        :param entity_id1: The id of the first entity.
        :param entity_id2: The id of the second entity.
        :return: The id of the new row or -1 if an error occurred.
        """
        logger.start(object={"table_name": table_name, "linked_table_name": linked_table_name, "entity_id1": entity_id1,
                             "entity_id2": entity_id2})

        combined_table_name = f"{table_name}_{linked_table_name}_table"
        combined_column_id = self.get_last_entry(
            table_name=table_name, linked_table_name=linked_table_name, entity_id1=entity_id1, entity_id2=entity_id2)[0][0] + 1
        data_json = {f"{table_name}_{linked_table_name}_id": combined_column_id,
                     f"{table_name}_id": entity_id1,
                     f"{linked_table_name}_id": entity_id2}
        self._validate_data_json(data_json)
        self._validate_table_name(table_name)
        validate_none_select_table_name(combined_table_name)
        columns = ','.join(data_json.keys())
        values = ','.join(['%s' for _ in data_json])
        insert_query = f"INSERT " + \
                       f"INTO {self.schema_name}.{combined_table_name} ({columns}) " \
                       f"VALUES ({values})"
        params = tuple(data_json.values())
        try:
            self.cursor.execute(insert_query, params)
            self.connection.commit()
            link_id = self.cursor.lastrowid()
            logger.end("Data inserted successfully.",
                       object={"link_id": link_id})
            return link_id
        except Exception as error:
            logger.exception(self._log_error_message(message="Error inserting data_json",
                                                     sql_statement=insert_query), object=error)
            logger.end()
            raise

    def delete_link(self, table_name: str, linked_table_name: str, entity_id1: int, entity_id2: int) -> None:
        """ Deletes a link between two entities."""
        logger.start(object={"table_name": table_name, "linked_table_name": linked_table_name, "entity_id1": entity_id1,
                             "entity_id2": entity_id2})

        combined_table_name = f"{table_name}_{linked_table_name}_table"

        # table_name = f"{table_name}_{linked_table_name}_table"
        where = f"{table_name}_id=%s AND {linked_table_name}_id=%s"
        params = (entity_id1, entity_id2)
        self._validate_table_name(combined_table_name)
        validate_none_select_table_name(combined_table_name)
        update_query = f"UPDATE {self.schema_name}.{combined_table_name} " \
                       f"SET end_timestamp=CURRENT_TIMESTAMP() " \
                       f"WHERE {where}"
        try:
            self.cursor.execute(update_query, params)
            self.connection.commit()
            logger.end("Deleted successfully.")

        except Exception as e:
            logger.exception(
                self._log_error_message(message="Error while deleting", sql_statement=update_query), object=e)
            logger.end()
            raise

    def get_last_entry(self, table_name: str, linked_table_name: str, entity_id1: int, entity_id2: int) -> int:
        """Returns the last entry of a link between two entities."""
        logger.start(object={"table_name": table_name, "linked_table_name": linked_table_name, "entity_id1": entity_id1,
                             "entity_id2": entity_id2})

        combined_table_name = f"{table_name}_{linked_table_name}_table"

        where = f"{table_name}_id=%s OR {linked_table_name}_id=%s"
        params = (entity_id1, entity_id2)
        self._validate_table_name(combined_table_name)
        validate_none_select_table_name(combined_table_name)
        select_query = f"SELECT {table_name}_{linked_table_name}_id " \
                       f"FROM {self.schema_name}.{combined_table_name} " \
                       f"WHERE {where} " \
                       f"ORDER BY {table_name}_{linked_table_name}_id  DESC " \
                       f"LIMIT 1"
        try:
            self.cursor.execute(select_query, params)
            result = self.cursor.fetchall()
            logger.end("Data selected successfully.")
            return result
        except Exception as e:
            logger.exception(
                self._log_error_message(message="Error while selecting", sql_statement=select_query), object=e)
            logger.end()
            raise
