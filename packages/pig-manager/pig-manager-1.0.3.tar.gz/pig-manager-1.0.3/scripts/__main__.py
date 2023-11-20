
import click
import os
import re
import subprocess
from tabulate import tabulate

def extract_and_print(output):
    """
    Function to extract only the relevant output and pretty-print it.
    """
    lines = output.split('\n')
    lines.reverse()

    # Regular expression for matching dates in the format YYYY-MM-DD
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

    extracted_lines = []
    for line in lines:
        if date_pattern.match(line):
            break
        extracted_lines.append(line)

    extracted_lines.reverse()

    table_data = []
    for line in extracted_lines:
        # Splitting the line at the comma and stripping extra characters
        columns = line.replace('(', '').replace(')', '').split(',')
        # Ensure that the second column (if exists) is treated as a string to retain precision
        columns = [col.strip() for col in columns]
        table_data.append(columns)

    # Print the data in a tabular format
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def run_command(command, dump_log, dump_out, dump_loc):
    """
    Runs the specified command with the given file.
    """
    try:
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        res, error = result.stdout, result.stderr

        if dump_out and res:
            with open(os.path.join(dump_loc, 'pig_output.txt'), 'w') as f:
                f.write(res)
        
        if dump_log and error:
            with open(os.path.join(dump_loc, 'pig_log.log'), 'w') as f:
                f.write(error)

        extract_and_print(res)

        print(f"Output and log dumped to {dump_loc}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")

@click.command()
@click.option('-f', '--file_path', prompt='File path', help='Path to the script file.')
@click.option('-dl', '--dump_log', is_flag=True, help='Flag to dump error output.')
@click.option('-do', '--dump_out', is_flag=True, help='Flag to dump standard output.')
@click.option('-l', '--dump_loc', default='.', help='Location to dump output and error files.')
def main(file_path, dump_log, dump_out, dump_loc):
    """
    CLI tool to run various commands (e.g., pig, hive, sql) and handle outputs.
    """
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    command = ['pig', '-x', 'local', '-e', open(file_path).read()]

    run_command(command, dump_log, dump_out, dump_loc)

if __name__ == '__main__':
    main()
