import pandas as pd
import tkinter as tk
from tkinter import filedialog

class CSVMergerApp:
    def __init__(self, master):
        self.master = master
        master.title("Melanj Fichye CSV")

        self.bouton_melanje = tk.Button(master, text="Melanj Fichye CSV", command=self.melanje_fichye_csv)
        self.bouton_melanje.pack(pady=30)

    def melanje_fichye_csv(self):
        fichye1 = filedialog.askopenfilename(title="Chwazi premye fichye CSV")
        fichye2 = filedialog.askopenfilename(title="Chwazi dezyèm fichye CSV")

        if not fichye1 or not fichye2:
            return

        try:
            Fich1 = pd.read_csv(fichye1)
            Fich2 = pd.read_csv(fichye2)
        except pd.errors.EmptyDataError:
            print("Erè: Youn oswa plizyè fichye yo vid.")
            return
        except pd.errors.ParserError:
            print("Erè: Kontni a nan yon oswa plizyè fichye yo pa bon format CSV.")
            return

        try:
            df_melanje = pd.concat([Fich1, Fich2], ignore_index=True)
        except ValueError:
            print("Erè: Nom kòlon ki idantik, se jis kondisyonere premye kolòn nan.")
            return

        fichye_sove = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichye CSV", "*.csv")])

        if not fichye_sove:
            return

        df_melanje.to_csv(fichye_sove, index=False)

        print(f"Melanj la kreye kòrèkteman. W'ap jwenn li nan '{fichye_sove}'")

        self.master.destroy()

if __name__ == "__main__":
    fenet = tk.Tk()
    app = CSVMergerApp(fenet)
    fenet.mainloop()
