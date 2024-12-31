import logging
import subprocess

# Pass a stderr output of a subprocess to the logging system.
def pass_stderr(stderr):

    if stderr == None or stderr == b'':
        return

    stderr_string = stderr.decode("utf-8")
    stderr_lines = stderr_string.splitlines()

    for line in stderr_lines:
        logging.warning(line)

# Construct a asciidoctor command.
def get_adoc_cmd(input, output, embedded, attributes):
    cmd = ["asciidoctor"]

    if embedded:
        cmd.append("-e")

    if attributes:
        cmd.append("-a")
        cmd.append(attributes)

    cmd.append("-o")
    cmd.append(output)
    cmd.append(input)

    logging.debug(f"constructed command \"{cmd}\"");

    return cmd

# Convert an adoc string to a html string.
def str_to_str(input, embedded, attributes):

    input_bytes = input.encode("utf-8")

    cmd = get_adoc_cmd("-", "-", embedded, attributes)
    process = subprocess.run(cmd, input=input_bytes, capture_output=True)
    pass_stderr(process.stderr)

    return process.stdout.decode("utf-8")

# Convert an adoc string to a html file.
def str_to_file(input, output_path, embedded, attributes):

    input_bytes = input.encode("utf-8")

    cmd = get_adoc_cmd("-", output_path, embedded, attributes)
    process = subprocess.run(cmd, input=input_bytes, capture_output=True)
    pass_stderr(process.stderr)

# Convert an adoc file to a html string.
def file_to_str(input_path, embedded, attributes):

    cmd = get_adoc_cmd(input_path, "-", embedded, attributes)
    process = subprocess.run(cmd, capture_output=True)
    pass_stderr(process.stderr)

    return process.stdout.decode("utf-8")

# Convert an adoc file to a html file.
def file_to_file(input_path, output_path, embedded, attributes):
    cmd = get_adoc_cmd(input_path, output_path, embedded, attributes)
    process = subprocess.run(cmd, capture_output=True)
    pass_stderr(process.stderr)
