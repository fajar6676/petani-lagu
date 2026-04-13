"""
File: farmlagu.py
Author: fajar6676 dan Nano Gi
Repo: https://github.com/fajar6676/urban-couscous
Description:dowload lagu youtube dengan mudah
Created: 2026-04-14
License: MIT
"""

import yt_dlp
import os
import subprocess
import shutil
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# ==========================================
# KONFIGURASI & IDENTITAS FINAL
# ==========================================
console = Console()
SAVE_PATH = 'C:/Users/Public/Music/Olike_Universal'
FFMPEG_EXE = shutil.which('ffmpeg') or shutil.which('ffmpeg.exe')

def get_logo():
    return """
 [bold yellow]    _   __                     ____                                [/bold yellow]
 [bold yellow]   / | / /___ _____  ____     / __ )____ _____  ____ _____  ____ _ [/bold yellow]
 [bold green]  /  |/ / __ `/ __ \/ __ \   / __  / __ `/ __ \/ __ `/ __ \/ __ `/ [/bold green]
 [bold green] / /|  / /_/ / / / / /_/ /  / /_/ / /_/ / / / / /_/ / / / / /_/ /  [/bold green]
 [bold white]/_/ |_/\__,_/_/ /_/\____/  /____/\__,_/_/ /_/\__,_/_/ /_/\__,_/   [/bold white]
    """

def clean_filename(name):
    name = name.replace("mentah_", "")
    name = re.sub(r'[^\w\s\.-]', '', name)
    return " ".join(name.split())[:50].strip()

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    ff_status = "[bold green]ACTIVE[/bold green]" if FFMPEG_EXE else "[bold red]OFFLINE[/bold red]"
    jml_lagu = 0
    if os.path.exists(SAVE_PATH):
        jml_lagu = len([f for f in os.listdir(SAVE_PATH) if f.endswith('.mp3')])
    
    console.print(Align.center(get_logo()))
    console.print(Align.center("[bold cyan]>>> PETANI LAGU DIGITAL - by FAJAR dan NANO GI <<<[/bold cyan]"))
    status_text = f"FFmpeg: {ff_status}  |  Gudang: [yellow]{jml_lagu} Lagu[/yellow]  |  speker Mode: [green]ON[/green]"
    console.print(Align.center(status_text))
    console.print(Align.center("[blue]" + "━"*60 + "[/blue]\n"))

def get_ydl_opts(batas_mb, mode_borongan=False):
    return {
        'ffmpeg_location': FFMPEG_EXE or '',
        'format': 'bestaudio/best',
        'noplaylist': not mode_borongan,
        'quiet': True, 'no_warnings': True, 'noprogress': True,
        'max_filesize': int(batas_mb) * 1024 * 1024,
        'outtmpl': f'{SAVE_PATH}/mentah_%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
    }

def cuci_lagu_pro():
    if not os.path.exists(SAVE_PATH): return
    files = [f for f in os.listdir(SAVE_PATH) if f.startswith("mentah_") and f.endswith(".mp3")]
    if not files: return

    table = Table(title="\n[bold green]📊 LAPORAN PENGULEKAN SUARA[/bold green]", show_header=True, header_style="bold magenta")
    table.add_column("No", justify="center", style="cyan")
    table.add_column("Judul Lagu", style="white")
    table.add_column("Hasil", justify="center")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as progress:
        task = progress.add_task("[cyan]Processing (Mono + Loudnorm)...", total=len(files))
        for i, filename in enumerate(files, 1):
            path_mentah = os.path.join(SAVE_PATH, filename)
            nama_bersih = f"{clean_filename(filename)}.mp3"
            path_hasil = os.path.join(SAVE_PATH, nama_bersih)
            
            cmd = [FFMPEG_EXE or 'ffmpeg.exe', '-i', path_mentah, '-af', 'pan=mono|c0=0.5*c0+0.5*c1,loudnorm', '-ar', '44100', '-ab', '128k', '-y', path_hasil]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
                os.remove(path_mentah)
                table.add_row(str(i), nama_bersih, "[bold green]BERHASIL[/bold green]")
            except:
                table.add_row(str(i), nama_bersih, "[bold red]GAGAL[/bold red]")
            progress.update(task, advance=1)
    console.print(table)

def menu_utama():
    if not os.path.exists(SAVE_PATH): os.makedirs(SAVE_PATH)
    while True:
        print_header()
        menu_table = Table.grid(padding=(0,2))
        menu_table.add_row("1", "Panen Otomatis (nama penyanyi/gendre)")
        menu_table.add_row("2", "Ambil via Link")
        menu_table.add_row("3", "Borong Channel/Playlist(salin link akun youtube")
        menu_table.add_row("0", "[bold red]Keluar[/bold red]")
        console.print(Align.center(Panel(menu_table, title="[bold green]KONTROL PANEL[/bold green]", border_style="bright_blue", padding=(1, 1))))
        
        pilih = console.input("\n[bold]Pilih Menu: [/bold]")
        if pilih == "0": 
            console.print("\n[bold yellow] TERIMAKASIH SUDAH MENGGUNAKAN SCRIPT INI [/bold yellow]")
            console.print("\n[bold white]Author: [cyan] FAJAR DAN NANO GI [/cyan][/bold white]")
            break
        if pilih in ["1", "2", "3"]:
            batas = console.input("[cyan]Batas Ukuran (MB) [Default 10]: [/cyan]") or "10"
            opts = get_ydl_opts(batas, mode_borongan=(pilih=="3"))
            
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    if pilih == "1":
                        kw = console.input("[green]Cari lagu apa? : [/green]")
                        target_jml = int(console.input("[green]Jumlah lagu? [Default 5]: [/green]") or "5")
                        
                        console.print(f"\n[bold yellow]🔍 AI Memindai 100+ kandidat untuk [white]{kw}[/white]...[/bold yellow]")
                        
                        # TAHAP 1: Cari kandidat 4x lipat lebih banyak
                        search_query = f"ytsearch{target_jml * 4}:{kw} official audio -cover -ai -robot"
                        info = ydl.extract_info(search_query, download=False)
                        
                        daftar_panen = []
                        blacklist = ["reaction", "podcast", "review", "vlog", "kondangan", "interview", "pembahasan", "full album", "koleksi", "kejutan"]
                        
                        if 'entries' in info:
                            for entry in info['entries']:
                                if len(daftar_panen) >= target_jml: break
                                
                                title = entry.get('title', '').lower()
                                desc = entry.get('description', '').lower()
                                duration = entry.get('duration', 0)
                                
                                # Verifikasi AI (Ganas)
                                is_clean = not any(word in title or word in desc for word in blacklist)
                                
                                if is_clean and 130 < duration < 480:
                                    daftar_panen.append(entry['webpage_url'])
                                    console.print(f"[bold green]✓[/bold green] [dim]{entry['title'][:55]}...[/dim]")
                        
                        # TAHAP 2: Download hasil seleksi
                        if daftar_panen:
                            console.print(f"\n[bold blue]🚜 Mengangkut {len(daftar_panen)} lagu pilihan ke gudang...[/bold blue]")
                            for link in daftar_panen:
                                ydl.download([link])
                        else:
                            console.print("[bold red]❌ Gagal: Tidak ada lagu yang lolos sensor AI.[/bold red]")

                    elif pilih == "2" or pilih == "3":
                        link = console.input("[green]Masukkan Link: [/green]")
                        ydl.download([link])
                
                cuci_lagu_pro()
                console.print("\n[bold green]🔔 Notifikasi: Panen Raya Selesai![/bold green]")
                console.input("\n[bold]Enter untuk kembali...[/bold]")
            except Exception as e:
                console.print(f"[bold red]Mesin Mogok: {e}[/bold red]")
                console.input("\nEnter untuk lanjut...")

if __name__ == "__main__":
    menu_utama()
                
