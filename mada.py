import tkinter as tk
from tkinter import messagebox, Toplevel
import json
import os

# Calea fișierului pentru salvarea datelor
FILE_PATH = "cheltuieli.json"
LIMITE_PATH = "limita.json"  # Fișier pentru salvarea limitei maxime

# Funcții pentru manipularea datelor

def incarca_date(cale):
    if os.path.exists(cale):
        try:
            with open(cale, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def salveaza_date(cale, date):
    with open(cale, "w", encoding="utf-8") as file:
        json.dump(date, file, indent=4)

def calculeaza_total():
    cheltuieli = incarca_date(FILE_PATH)
    return sum(float(c["suma"]) for c in cheltuieli)

# Funcții pentru cheltuieli

def adauga_cheltuiala():
    suma = suma_entry.get()
    descriere = descriere_entry.get()

    if suma.strip() and descriere.strip():
        try:
            suma_float = float(suma)
            cheltuieli = incarca_date(FILE_PATH)
            cheltuieli.append({"suma": suma_float, "descriere": descriere})
            salveaza_date(FILE_PATH, cheltuieli)
            messagebox.showinfo("Succes", "Cheltuiala a fost adăugată!")
            suma_entry.delete(0, tk.END)
            descriere_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Eroare", "Introdu o sumă validă!")
    else:
        messagebox.showwarning("Eroare", "Completează toate câmpurile!")


def vizualizeaza_cheltuieli():
    cheltuieli = incarca_date(FILE_PATH)
    if cheltuieli:
        mesaj = "\n".join([f"Suma: {c['suma']} RON | Descriere: {c['descriere']}" for c in cheltuieli])
        total = calculeaza_total()
        mesaj += f"\n\nSuma totală: {total:.2f} RON"
        messagebox.showinfo("Cheltuielile Tale", mesaj)
    else:
        messagebox.showinfo("Cheltuieli", "Nu există cheltuieli salvate.")


def sterge_cheltuieli():
    confirmare = messagebox.askyesno("Confirmare", "Sigur vrei să ștergi toate cheltuielile?")
    if confirmare:
        salveaza_date(FILE_PATH, [])
        messagebox.showinfo("Succes", "Toate cheltuielile au fost șterse!")

# Funcții pentru limită

def seteaza_limita():
    def salveaza_limita():
        limita = limita_entry.get()
        if limita.strip():
            try:
                limita_float = float(limita)
                salveaza_date(LIMITE_PATH, {"limita": limita_float})
                messagebox.showinfo("Succes", f"Limita a fost setată la {limita_float:.2f} RON")
                fereastra_limita.destroy()
            except ValueError:
                messagebox.showwarning("Eroare", "Introdu o sumă validă!")
        else:
            messagebox.showwarning("Eroare", "Completează câmpul!")

    fereastra_limita = Toplevel(app)
    fereastra_limita.title("Setare Limită")
    fereastra_limita.geometry("300x150")

    tk.Label(fereastra_limita, text="Introdu limita maximă (RON):", font=("Arial", 12)).pack(pady=10)
    limita_entry = tk.Entry(fereastra_limita, font=("Arial", 12))
    limita_entry.pack(pady=5)
    tk.Button(fereastra_limita, text="Salvează", command=salveaza_limita, bg="lightgreen", font=("Arial", 12)).pack(pady=10)


def verifica_limita():
    total = calculeaza_total()
    limita = incarca_date(LIMITE_PATH).get("limita")

    if limita is not None:
        limita = float(limita)
        if total > limita:
            depasire = total - limita
            procent = (depasire / limita) * 100
            messagebox.showwarning("Atenție!", f"Ai depășit limita cu {depasire:.2f} RON ({procent:.2f}%)")
        else:
            messagebox.showinfo("Info", f"Ești încă sub limită! Suma totală: {total:.2f} RON")
    else:
        messagebox.showwarning("Eroare", "Nu a fost setată nicio limită. Setează una!")

# Inițializarea aplicației Tkinter
app = tk.Tk()
app.title("Manager Cheltuieli Lunare")
app.geometry("400x400")
app.config(bg="lightgrey")

# Etichete și câmpuri pentru input
tk.Label(app, text="Suma (RON):", bg="lightgrey", font=("Arial", 12)).pack(pady=5)
suma_entry = tk.Entry(app, font=("Arial", 12))
suma_entry.pack(pady=5)

tk.Label(app, text="Descriere:", bg="lightgrey", font=("Arial", 12)).pack(pady=5)
descriere_entry = tk.Entry(app, font=("Arial", 12))
descriere_entry.pack(pady=5)

# Butoane pentru funcționalități
tk.Button(app, text="Adaugă Cheltuială", bg="lightgreen", font=("Arial", 12), command=adauga_cheltuiala).pack(pady=10)
tk.Button(app, text="Vizualizează Cheltuieli", bg="lightblue", font=("Arial", 12), command=vizualizeaza_cheltuieli).pack(pady=10)
tk.Button(app, text="Șterge Toate Cheltuielile", bg="lightcoral", font=("Arial", 12), command=sterge_cheltuieli).pack(pady=10)
tk.Button(app, text="Setează Limită", bg="gold", font=("Arial", 12), command=seteaza_limita).pack(pady=10)
tk.Button(app, text="Verifică Limită", bg="orange", font=("Arial", 12), command=verifica_limita).pack(pady=10)

# Rulare aplicație
app.mainloop()
