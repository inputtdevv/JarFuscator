import os
import sys
import subprocess
import random
import string
from pystyle import Colorate, Colors
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

Libs = [
    "utilities/asm-9.6.jar",
    "utilities/asm-tree-9.6.jar",
    "utilities/asm-commons-9.6.jar"
]

file = "JarFuscation.java"
logo = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⣼⣿⡗⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀
⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦
⠀⠀⢱⡀⠀⠉⠉⠀⠀⠀⠀⠛⠃⠀⢠⡟⠀⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⢃⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
inputt.dev 💖
"""

def banner():
    print(Colorate.Horizontal(Colors.blue_to_white, logo))
    print(f"\n{Fore.GREEN}(+) Inputt.dev{Style.RESET_ALL}\n")

def randstr(n=6):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def compiler():
    if not os.path.isfile(file):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Obfuscator code ({file}) not found!")
        sys.exit(1)
    cp = os.pathsep.join(["."] + Libs)
    subprocess.run(["javac", "-cp", cp, file], check=True)

def start(input_jar, output_name=None, libs=None, phantom=False, notrack=False, exempt=None, runtime=None, fuckit=False):
    cp = os.pathsep.join(["."] + (libs.split(os.pathsep) if libs else Libs))
    if not output_name:
        output_name = f"jarfuscator-{randstr()}.jar"
    engine_class = os.path.splitext(os.path.basename(file))[0]
    
    cmd = ["java", "-cp", cp, engine_class, input_jar, output_name]
    if phantom: cmd.append("--phantom")
    if notrack: cmd.append("--notrack")
    if exempt: cmd.append(f"--exempt={exempt}")
    if runtime: cmd.append(f"--runtime={runtime}")
    if fuckit: cmd.append("--fuckit")
    
    subprocess.run(cmd, check=True)
    return output_name

def clean():
    for f in os.listdir("."):
        if f.endswith(".class"):
            try:
                os.remove(f)
            except:
                pass

def parse_args():
    args = {
        "input": None, "output": None, "libs": None, "phantom": False, 
        "notrack": False, "exempt": None, "runtime": None, "fuckit": False, "help": False
    }
    for arg in sys.argv[1:]:
        if arg.startswith("--output="): args["output"] = arg.split("=",1)[1]
        elif arg.startswith("--libs="): args["libs"] = arg.split("=",1)[1]
        elif arg=="--phantom": args["phantom"]=True
        elif arg=="--notrack": args["notrack"]=True
        elif arg.startswith("--exempt="): args["exempt"]=arg.split("=",1)[1]
        elif arg.startswith("--runtime="): args["runtime"]=arg.split("=",1)[1]
        elif arg=="--fuckit": args["fuckit"]=True
        elif arg=="--help": args["help"]=True
        elif not args["input"]: args["input"]=arg
    return args

def interactive_input(args):
    if not args["input"]:
        args["input"] = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Input JAR path: ").strip()
        if not args["input"].lower().endswith(".jar"): args["input"] += ".jar"
    if not os.path.isfile(args["input"]):
        print(f"{Fore.RED}[FILE NOT FOUND]{Style.RESET_ALL} File not found: {args['input']}")
        sys.exit(1)
    if not args["output"]:
        args["output"] = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Output JAR path (leave blank for random): ").strip()
        if args["output"]=="": args["output"]=None
    return args

if __name__=="__main__":
    args = parse_args()
    banner()
    if args["help"]:
        print(f"""
JarFuscator, Inputt.dev
<input>           Path to your input JAR
--output=<output> Output path
--libs=<libs>     Path to dependencies folder
--phantom         Enable phantom computation
--notrack         Disable analytics
--exempt=<file>   Exclusions list
--runtime=<path>  Java runtime path
--fuckit          Skip critical computation (use at your own risk)
--help            Show this help
""")
        sys.exit(0)
    args = interactive_input(args)
    compiler()
    out = start(
        args["input"], args["output"], libs=args["libs"], phantom=args["phantom"],
        notrack=args["notrack"], exempt=args["exempt"], runtime=args["runtime"], fuckit=args["fuckit"]
    )
    clean()
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Output: {out}")
    input("Press Enter to exit...")
    sys.exit(0)
