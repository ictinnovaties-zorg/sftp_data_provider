from pathlib import Path
import argparse
import sys
import subprocess

try: 
    input_mermaid_index = sys.argv.index("-i") + 1
    input_mermaid_file = Path(sys.argv[input_mermaid_index]).resolve()
    sys.argv[input_mermaid_index] = input_mermaid_file.name
except ValueError:
    print("ERROR: No input file passed using -i")
    sys.exit(1)

docker_call = ['docker', 'run', '--rm', 
  '-v', str(input_mermaid_file.resolve().parent) + ':/data', 
  'minlag/mermaid-cli']
docker_call.extend(sys.argv[1:])
subprocess.run(docker_call)