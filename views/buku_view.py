import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("1100x600")

        # Konfigurasi grid utama: form di kiri dan tabel di kanan
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Frame kiri untuk formulir
        self.frame_kiri = ctk.CTkScrollableFrame(self)
        self.frame_kiri.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Buku",
            font=("Arial", 16, "bold"),
        ).pack(pady=15)

        # Input buku
        self.entry_isbn = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="ISBN (opsional)",
        )
        self.entry_isbn.pack(pady=8, padx=15, fill="x")

        self.entry_judul = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Judul Buku",
        )
        self.entry_judul.pack(pady=8, padx=15, fill="x")

        self.entry_penulis = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Penulis",
        )
        self.entry_penulis.pack(pady=8, padx=15, fill="x")

        self.entry_kategori = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Kategori Buku",
        )
        self.entry_kategori.pack(pady=8, padx=15, fill="x")

        self.entry_tahun = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Tahun Terbit (opsional)",
        )
        self.entry_tahun.pack(pady=8, padx=15, fill="x")

        self.entry_stok = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Stok (kosong = 0)",
        )
        self.entry_stok.pack(pady=8, padx=15, fill="x")

        # Tombol aksi
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color="green",
        )
        self.btn_simpan.pack(pady=(18, 8), padx=15, fill="x")

        self.btn_update = ctk.CTkButton(
            self.frame_kiri,
            text="Update Data",
            fg_color="blue",
        )
        self.btn_update.pack(pady=8, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data",
            fg_color="red",
        )
        self.btn_hapus.pack(pady=8, padx=15, fill="x")

        # Frame kanan untuk tabel
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(
            row=0, column=1, padx=10, pady=10, sticky="nsew"
        )
        self.frame_kanan.grid_columnconfigure(0, weight=1)
        self.frame_kanan.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Koleksi Buku",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, pady=15)

        # Tabel dengan kolom yang sesuai dengan tabel database books
        kolom = (
            "id",
            "isbn",
            "title",
            "author",
            "category",
            "publication_year",
            "stock",
        )

        self.tabel = ttk.Treeview(
            self.frame_kanan,
            columns=kolom,
            show="headings",
        )

        self.tabel.heading("id", text="ID")
        self.tabel.heading("isbn", text="ISBN")
        self.tabel.heading("title", text="Judul")
        self.tabel.heading("author", text="Penulis")
        self.tabel.heading("category", text="Kategori")
        self.tabel.heading("publication_year", text="Tahun Terbit")
        self.tabel.heading("stock", text="Stok")

        self.tabel.column("id", width=50, anchor="center")
        self.tabel.column("isbn", width=120, anchor="center")
        self.tabel.column("title", width=180)
        self.tabel.column("author", width=150)
        self.tabel.column("category", width=120)
        self.tabel.column("publication_year", width=100, anchor="center")
        self.tabel.column("stock", width=70, anchor="center")

        # Scrollbar vertikal dan horizontal untuk tabel
        scrollbar_y = ttk.Scrollbar(
            self.frame_kanan,
            orient="vertical",
            command=self.tabel.yview,
        )
        scrollbar_x = ttk.Scrollbar(
            self.frame_kanan,
            orient="horizontal",
            command=self.tabel.xview,
        )

        self.tabel.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
        )

        self.tabel.grid(row=1, column=0, sticky="nsew", padx=(15, 0))
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scrollbar_x.grid(row=2, column=0, sticky="ew", padx=(15, 0))


if __name__ == "__main__":
    app = BukuView()
    app.mainloop()