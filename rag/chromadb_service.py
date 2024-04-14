import argparse
import getpass
import subprocess

def run(args):
    cmd = [f"chroma run --path {args.db_path}"]
    if args.detach:
        subprocess.Popen(cmd, shell=True, start_new_session=True)
        print("chromadb service detached.")
    else:
        subprocess.run(cmd, shell=True)

def abort(args):
    sudo_passwd = getpass.getpass(prompt="Password: ").encode()
    print(f"Get services on port {args.port}")
    proc = subprocess.Popen(['sudo','lsof', '-i', f":{args.port}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, _ = proc.communicate(input=sudo_passwd)
    
    stdout_lines= output.decode().split("\n")
    pids = []
    stdout_lines = [line for line in stdout_lines if line]
    for line in stdout_lines:
        pids.append(line.split(' ')[1])
    pids = set([pid for pid in pids if pid])
    print(f"port uses pid: {pids}")

    is_kill = getpass.getpass(prompt="Are you sure to kill? y/[N]")
    if is_kill.lower() in ["y", "yes"]:
        for pid in pids:
            proc = subprocess.Popen(['sudo', 'kill', '-9', f'{pid}'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            output, _ = proc.communicate(input=sudo_passwd)
            print(f"process killed : {pid}")
    else:
        print("process not killed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db_path", type=str, default="./vector_store")
    parser.add_argument("--port", type=str, default="8000")
    parser.add_argument("--exec", choices=["run", "stop"], type=str)
    parser.add_argument("--detach", action="store_true", default=True)
    args = parser.parse_args()

    if args.exec == "run":
        run(args)
    else:
        abort(args)