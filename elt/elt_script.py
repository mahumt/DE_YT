import subprocess # to be able to contorl I/O
import time

# this function is a 2nd failsafe to ensure the elt dosent run before postgres
# first failsafe is in the docker-compose.yaml
def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Successfully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting.")
    return False


# Use the function before running the ELT process
if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("START: Starting ELT script...")

# Configuration for the source PostgreSQL database using dump files

source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'source_postgres'
}

# Configuration for the destination PostgreSQL database
destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'destination_postgres'
}

# Use pg_dump to dump the source database to a SQL file
dump_command = [
    'pg_dump',                      # this is the command in postgres to create the dump file
    '-h', source_config['host'],    # host
    '-U', source_config['user'],    # user
    '-d', source_config['dbname'],  # database name
    '-f', 'data_dump.sql',          # the file that is going to be for the dump "outfile"
    # https://www.postgresql.org/docs/8.1/backup.html#BACKUP-DUMP-RESTORE
    '-w'                            # Do not prompt for password
]


# Set the PGPASSWORD environment variable to avoid password prompt (related to the 'w' in dump command)
subprocess_env = dict(PGPASSWORD = source_config['password'])

# Execute the dump command
subprocess.run(dump_command, env = subprocess_env, check = True)

# Use psql to load the dumped SQL file into the destination database
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', 
    '-f', 'data_dump.sql'
]

# Set the PGPASSWORD environment variable for the destination database
subprocess_env = dict(PGPASSWORD = destination_config['password'])

# Execute the load command
subprocess.run(load_command, env=subprocess_env, check=True)

print("DONE: Ending ELT script...")