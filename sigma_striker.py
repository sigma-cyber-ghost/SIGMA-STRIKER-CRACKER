import os
import subprocess
import time
import itertools
from pathlib import Path
from tkinter import Tk, filedialog, messagebox, simpledialog
from termcolor import cprint, colored
from colorama import init
import pikepdf
from tqdm import tqdm

init()

BANNER_ART = """
\033[1;31m⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[0m
"""

SOCIALS = {
    "📱 Telegram": "https://web.telegram.org/k/#@Sigma_Cyber_Ghost",
    "🐱 GitHub  ": "https://github.com/sigma-cyber-ghost",
    "📺 YouTube ": "https://www.youtube.com/@sigma_ghost_hacking"
}

SUPPORTED = [".rar", ".zip", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", ".zst", ".001", ".lz", ".cab", ".jar", ".arj", ".uue", ".zipx", ".pdf"]

def animate(text, delay=0.01):
    for char in text:
        print(colored(char, 'cyan'), end='', flush=True)
        time.sleep(delay)
    print()

def loading_spinner(text, duration=2):
    spinner = ['⠁','⠂','⠄','⡀','⢀','⠠','⠐','⠈']
    t_end = time.time() + duration
    idx = 0
    while time.time() < t_end:
        print(f"\r{colored(text, 'yellow')} {spinner[idx % len(spinner)]}", end='', flush=True)
        idx += 1
        time.sleep(0.1)
    print()

def display_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(BANNER_ART)
    cprint("SIGMA STRIKER — STREAM-FORCE BLACK HAT HACKER EDITION", "red", attrs=["bold"])
    cprint("="*60, "cyan")
    for label, link in SOCIALS.items():
        print(f"{colored(label, 'yellow')} {colored(link, 'cyan')}")
    cprint("="*60, "cyan")

def ask_file():
    root = Tk(); root.withdraw()
    messagebox.showinfo("SIGMA STRIKER", "Select archive file to crack")
    return filedialog.askopenfilename()

def ask_mode():
    root = Tk(); root.withdraw()
    return messagebox.askquestion("MODE", "Generate passwords on the fly?") == "yes"

def ask_charset():
    root = Tk(); root.withdraw()
    options = {
        "1": "0123456789",
        "2": "abcdefghijklmnopqrstuvwxyz",
        "3": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "4": "@#$%&*?!",
        "5": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*?!"
    }
    choice = simpledialog.askstring("Charset", "Choose charset:\n1 = numbers\n2 = lowercase\n3 = uppercase\n4 = symbols\n5 = combo")
    return options.get(choice, options["5"])

def ask_length_range():
    root = Tk(); root.withdraw()
    min_len = simpledialog.askinteger("Length", "Minimum password length:")
    max_len = simpledialog.askinteger("Length", "Maximum password length:")
    return min_len, max_len

def ask_wordlist():
    root = Tk(); root.withdraw()
    messagebox.showinfo("SIGMA STRIKER", "Select your custom wordlist")
    return filedialog.askopenfilename()

def get_ext(file_path):
    return ''.join(Path(file_path).suffixes).lower()

def create_output_dir(archive_path):
    name = Path(archive_path).stem
    output_dir = f"crack_{name}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def try_passwords(file_path, generate=False, charset=None, min_len=0, max_len=0, wordlist=None):
    ext = get_ext(file_path)
    if not ext or not any(e in ext for e in SUPPORTED):
        cprint(f"[X] Unsupported file type: {ext}", "red")
        return

    is_pdf = ".pdf" in ext
    output_dir = create_output_dir(file_path) if not is_pdf else None

    base_cmd = f'unrar x -y -pPASSWORD "{file_path}" "{output_dir}/"' if ".rar" in ext \
        else f'7z x -y -o"{output_dir}" -pPASSWORD "{file_path}"'

    def try_pass(pwd):
        if is_pdf:
            try:
                with pikepdf.open(file_path, password=pwd) as pdf:
                    pdf.save(f'unlocked_{Path(file_path).name}')
                return True
            except pikepdf.PasswordError:
                return False
        else:
            cmd = base_cmd.replace("PASSWORD", pwd)
            result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0

    cprint(f"[+] Target: {file_path}", "green")
    loading_spinner("Brute engine engaged")

    if generate:
        for length in range(min_len, max_len + 1):
            for pwd_tuple in tqdm(itertools.product(charset, repeat=length), desc=f"Len {length}"):
                pwd = ''.join(pwd_tuple)
                print(colored(f"[-] Trying: {pwd}", "blue"))
                if try_pass(pwd):
                    cprint(f"[✓] Cracked: {pwd}", "green", attrs=["bold"])
                    with open("/tmp/sigma_vault.txt", "a") as vault:
                        vault.write(f"{file_path} => {pwd}\n")
                    cprint(f"[✓] {'PDF Unlocked' if is_pdf else f'Extracted to: {output_dir}/'}", "cyan")
                    return
        cprint("[!] No match found in generated stream.", "red")
    else:
        with open(wordlist, 'r', errors="ignore") as f:
            for pwd in f:
                pwd = pwd.strip()
                if not pwd:
                    continue
                print(colored(f"[-] Trying: {pwd}", "blue"))
                if try_pass(pwd):
                    cprint(f"[✓] Cracked: {pwd}", "green", attrs=["bold"])
                    with open("/tmp/sigma_vault.txt", "a") as vault:
                        vault.write(f"{file_path} => {pwd}\n")
                    cprint(f"[✓] {'PDF Unlocked' if is_pdf else f'Extracted to: {output_dir}/'}", "cyan")
                    return
        cprint("[!] Password not found in wordlist.", "red")

if __name__ == "__main__":
    display_banner()
    archive = ask_file()
    if ask_mode():
        charset = ask_charset()
        min_len, max_len = ask_length_range()
        try_passwords(archive, generate=True, charset=charset, min_len=min_len, max_len=max_len)
    else:
        wordlist = ask_wordlist()
        try_passwords(archive, generate=False, wordlist=wordlist)
