import os
import subprocess
import sys

from datasphere.auth import env, ServerEnv

# We use this Python script (instead of plain bash command) for launching execution to have debug.

if __name__ == '__main__':
    os.chdir(f'scenarios/{os.environ["SCENARIO"]}')
    subprocess.run([
        sys.executable,
        '-m', 'datasphere.main',
        '-t', os.getenv('YC_OAUTH_TOKEN', ''),
        'project', 'job', 'execute',
        '--project-id', 'bt146eeguefuqa2fgfl9' if env == ServerEnv.PROD else 'b3pbocd5dua07ojecibq',
        '-c', 'config.yaml',
    ])
