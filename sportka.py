# Importy a knihovny
import ttkbootstrap as ttkb  # Pro moderní vzhled GUI
from ttkbootstrap.constants import *  # Konstanty pro styly
import tkinter as tk  # Pro základní GUI
from tkinter import messagebox  # Pro zobrazování chybových hlášení
import itertools  # Pro generování kombinací
import random  # Pro náhodné operace

# ----------------------------------
# Logika pro generování sázenek
# ----------------------------------

# Funkce pro generování sázenek
def generuj_sazenky():
    try:
        # Získání a kontrola hodnot z GUI
        vlastni_cisla = [int(c.strip()) for c in vlastni_cisla_entry.get().split(",") if c.strip().isdigit()]
        max_cislo = int(max_cislo_entry.get())  # Maximální číslo v loterii
        delka_sloupce = int(delka_sloupce_entry.get())  # Počet čísel v jednom sloupci
        vlastni_ve_sloupci = int(vlastni_ve_sloupci_entry.get())  # Počet vlastních čísel ve sloupci
        cena_za_sloupec = float(cena_za_sloupec_entry.get())  # Cena za jeden sloupec
        pocet_sloupcu = pocet_sloupcu_entry.get()  # Počet sloupců, pokud je prázdný, použije se max

        # Kontrola validních vstupů
        if vlastni_ve_sloupci > delka_sloupce:
            messagebox.showerror("Chyba", "Počet vlastních čísel ve sloupci nesmí být větší než délka sloupce.")
            return

        if len(vlastni_cisla) < vlastni_ve_sloupci:
            messagebox.showerror("Chyba", "Nemáš dost vlastních čísel pro daný počet ve sloupci.")
            return

        if max(vlastni_cisla) > max_cislo:
            messagebox.showerror("Chyba", "Tvoje čísla nesmí být větší než maximální číslo.")
            return

        # Generování kombinací čísel pro sázenky
        vsechna_cisla = set(range(1, max_cislo + 1))  # Všechna čísla od 1 do max_cislo
        kombinace = []  # Seznam pro ukládání všech kombinací
        vsechny_vlastni_kombinace = list(itertools.combinations(vlastni_cisla, vlastni_ve_sloupci))  # Kombinace vlastních čísel

        # Generování náhodných čísel pro každou kombinaci
        for vlastni_k in vsechny_vlastni_kombinace:
            zbyla_cisla = sorted(vsechna_cisla - set(vlastni_k))  # Zbývající čísla po odečtení vlastních
            pocet_nahodnych = delka_sloupce - len(vlastni_k)  # Počet náhodných čísel
            nahodne_k = list(itertools.combinations(zbyla_cisla, pocet_nahodnych))  # Vygenerujeme kombinace zbylých čísel
            for nahodna in random.sample(nahodne_k, min(len(nahodne_k), 20)):  # Náhodně vybereme až 20 kombinací
                kombinace.append(list(vlastni_k) + list(nahodna))  # Přidáme kombinaci vlastních a náhodných čísel

        # Zmíchání kombinací pro větší náhodnost
        random.shuffle(kombinace)

        # Pokud je zadán počet sloupců, omezíme počet kombinací
        if pocet_sloupcu:
            kombinace = kombinace[:int(pocet_sloupcu)]

        # Výpočet celkové ceny
        celkova_cena = cena_za_sloupec * len(kombinace)

        # ----------------------------------
        # GUI pro zobrazení výsledků
        # ----------------------------------

        # Aktualizace GUI pro zobrazení sázenek
        text_output.config(state=tk.NORMAL)  # Povolení úpravy textového pole
        text_output.delete("1.0", tk.END)  # Vymazání předchozího výstupu
        for index, k in enumerate(kombinace, start=1):
            random.shuffle(k)  # Zmícháme čísla ve sloupci pro větší náhodnost
            text_output.insert(tk.END, f"{k} - Cena za sloupec: {cena_za_sloupec * index:.2f} Kč\n")  # Zobrazíme kombinaci s cenou
        text_output.config(state=tk.DISABLED)  # Opět nastavíme textové pole na pouze pro čtení

        # Zobrazení počtu generovaných kombinací a celkové ceny
        label_count.config(text=f"Vygenerováno kombinací: {len(kombinace)}")
        label_total_cost.config(text=f"Celková cena: {celkova_cena:.2f} Kč")

    except Exception as e:
        messagebox.showerror("Chyba", f"Nastala chyba: {e}")

# Funkce pro smazání výstupu
def smazat_vystup():
    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    label_count.config(text="")
    label_total_cost.config(text="")
    text_output.config(state=tk.DISABLED)


# ----------------------------------
# GUI - Uživatelské rozhraní
# ----------------------------------

# Inicializace hlavního okna
root = ttkb.Window(themename="flatly")
root.title("Sázenka Generátor by Jan Galba V0.1")
root.geometry("1000x1200")
#root.iconbitmap("C:\\Users\\janga\\dist\\money.ico") # Změna ikony okna - i s cestou


# Tvorba layoutu pro vstupy a tlačítka
frame = ttkb.Frame(root, padding=10)
frame.pack(fill="x", pady=10)

ttkb.Label(frame, text="Tvoje čísla (oddělená čárkami):").grid(row=0, column=0, sticky="w")
vlastni_cisla_entry = ttkb.Entry(frame, width=60)
vlastni_cisla_entry.grid(row=0, column=1, columnspan=2, pady=5)

ttkb.Label(frame, text="Maximální číslo v loterii:").grid(row=1, column=0, sticky="w")
max_cislo_entry = ttkb.Entry(frame, width=10)
max_cislo_entry.grid(row=1, column=1, sticky="w", pady=5)

ttkb.Label(frame, text="Počet čísel v jednom sloupci:").grid(row=2, column=0, sticky="w")
delka_sloupce_entry = ttkb.Entry(frame, width=10)
delka_sloupce_entry.grid(row=2, column=1, sticky="w", pady=5)

ttkb.Label(frame, text="Kolik vlastních čísel má být ve sloupci:").grid(row=3, column=0, sticky="w")
vlastni_ve_sloupci_entry = ttkb.Entry(frame, width=10)
vlastni_ve_sloupci_entry.grid(row=3, column=1, sticky="w", pady=5)

ttkb.Label(frame, text="Cena za sloupec:").grid(row=4, column=0, sticky="w")
cena_za_sloupec_entry = ttkb.Entry(frame, width=10)
cena_za_sloupec_entry.grid(row=4, column=1, sticky="w", pady=5)

ttkb.Label(frame, text="Počet sloupců (prázdné = max):").grid(row=5, column=0, sticky="w")
pocet_sloupcu_entry = ttkb.Entry(frame, width=10)
pocet_sloupcu_entry.grid(row=5, column=1, sticky="w", pady=5)

# Tlačítka pro generování a smazání
ttkb.Button(frame, text="\U0001F3B2 Generuj kombinace", command=generuj_sazenky, bootstyle="success")\
    .grid(row=6, column=0, columnspan=2, pady=5)
ttkb.Button(frame, text="\U0001F9F9 Smazání výstupu", command=smazat_vystup, bootstyle="danger")\
    .grid(row=6, column=2, pady=5)

# Label pro zobrazení počtu kombinací a celkové ceny
label_count = ttkb.Label(frame, text="")
label_count.grid(row=7, column=0, columnspan=3)

label_total_cost = ttkb.Label(frame, text="")
label_total_cost.grid(row=8, column=0, columnspan=3)

# Textové pole pro zobrazení výsledků
text_frame = ttkb.Frame(root)
text_frame.pack(fill="both", expand=True, padx=20, pady=10)

scrollbar = ttkb.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

text_output = tk.Text(text_frame, height=20, wrap="none", yscrollcommand=scrollbar.set, font=("Consolas", 10))
text_output.pack(side="left", fill="both", expand=True)
text_output.config(state=tk.DISABLED)
scrollbar.config(command=text_output.yview)

root.mainloop()
