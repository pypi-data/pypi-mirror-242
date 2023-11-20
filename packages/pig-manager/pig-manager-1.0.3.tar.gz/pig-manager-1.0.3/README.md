# Pig Manager

## Description
Pretty Printer for Pig Latin scripts.

## Installation
To install Pig Pretty Printer, simply use pip:
```bash
pip install pig-manager
```

## Usage
After installation, you can run pig-manager from the command line:
```
pig-manager -f <file> [options]
```

## Options
```
-f, --file_path: Path to the Pig script file.
-dl, --dump_log: Flag to dump error output.
-do, --dump_out: Flag to dump standard output.
-l, --dump_loc: Location to dump output and error files.
```

## Example
```
pig_pretty_printer -f path/to/your/script.pig -dl -do -l path/to/dump



```

## License
This project is licensed under the MIT License.
