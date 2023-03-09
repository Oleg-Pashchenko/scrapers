import psycopg2

from misc.secrets import secret_info


def create_oreht_table_statement():
    return """
            CREATE TABLE IF NOT EXISTS oreht_positions (
                id BIGINT NOT NULL,
                upload_date TIMESTAMP NOT NULL
            )
        """


def create_oreht_error_table_statement():
    return """
                CREATE TABLE IF NOT EXISTS oreht_error_positions (
                    id BIGINT NOT NULL,
                    upload_date TIMESTAMP NOT NULL, 
                    check_date TIMESTAMP NOT NULL
                )
            """


def create_ozon_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS ozon (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT,
            price FLOAT,
            creation_date TIMESTAMP NOT NULL
        )
    """


def create_wilberries_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS wilberries (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT,
            price FLOAT,
            creation_date TIMESTAMP NOT NULL
        )
    """


def create_ozon_error_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS ozon_error (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT,
            price FLOAT,
            creation_date TIMESTAMP NOT NULL,
            check_date TIMESTAMP NOT NULL
        )
    """

def create_wilberries_error_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS wilberries_error (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT,
            price FLOAT,
            creation_date TIMESTAMP NOT NULL,
            check_date TIMESTAMP NOT NULL 
        )
    """


def create_neural_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS neural (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT, 
            price FLOAT,
            source_id BIGINT NOT NULL,
            source_link TEXT,
            source_photo TEXT,
            source_name TEXT,
            source_price FLOAT,
            source_creation_date TIMESTAMP NOT NULL
        )
    """

def create_neural_error_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS neural_error (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT, 
            price FLOAT,
            source_id BIGINT NOT NULL,
            source_link TEXT,
            source_photo TEXT,
            source_name TEXT,
            source_price FLOAT,
            source_creation_date TIMESTAMP NOT NULL,
            check_date TIMESTAMP NOT NULL 
        )
    """

def create_presentation_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS presentation (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT, 
            price FLOAT,
            source_id BIGINT NOT NULL,
            source_link TEXT,
            source_photo TEXT,
            source_name TEXT,
            source_price FLOAT,
            source_creation_date TIMESTAMP NOT NULL
        )
    """


def create_presentation_error_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS presentation_error (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT, 
            price FLOAT,
            source_id BIGINT NOT NULL,
            source_link TEXT,
            source_photo TEXT,
            source_name TEXT,
            source_price FLOAT,
            source_creation_date TIMESTAMP NOT NULL,
            check_date TIMESTAMP NOT NULL 
        )
    """

def create_result_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS result (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT, 
            price FLOAT,
            source_id BIGINT NOT NULL,
            source_link TEXT,
            source_photo TEXT,
            source_name TEXT,
            source_price FLOAT,
            source_creation_date TIMESTAMP NOT NULL
        )
    """
def create_result_error_table_statement():
    return """
        CREATE TABLE IF NOT EXISTS result_error (
            id BIGINT NOT NULL,
            link TEXT,
            photo TEXT,
            name TEXT, 
            price FLOAT,
            source_id BIGINT NOT NULL,
            source_link TEXT,
            source_photo TEXT,
            source_name TEXT,
            source_price FLOAT,
            source_creation_date TIMESTAMP NOT NULL,
            check_date TIMESTAMP NOT NULL 
        )
    """


def initialize():
    conn = psycopg2.connect(host=secret_info.POSTGRES_HOST, database=secret_info.POSTGRES_DBNAME,
                            user=secret_info.POSTGRES_USER, password=secret_info.POSTGRES_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(create_oreht_table_statement())
    cursor.execute(create_oreht_error_table_statement())
    cursor.execute(create_ozon_table_statement())
    cursor.execute(create_wilberries_table_statement())
    cursor.execute(create_ozon_error_table_statement())
    cursor.execute(create_wilberries_error_table_statement())
    cursor.execute(create_neural_table_statement())
    cursor.execute(create_neural_error_table_statement())
    cursor.execute(create_presentation_table_statement())
    cursor.execute(create_presentation_error_table_statement())
    cursor.execute(create_result_table_statement())
    cursor.execute(create_result_error_table_statement())
    conn.commit()
    conn.close()
