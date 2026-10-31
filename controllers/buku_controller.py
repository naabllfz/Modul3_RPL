import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = BukuModel()
        self.view = BukuView()

        # Menghubungkan tombol Simpan dengan fungsi Controller
        self.view.btn_simpan.configure(command=self.simpan_data)

        # Memuat data saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Kosongkan isi tabel terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Ambil data buku dari Model
        data_buku = self.model.get_all_buku()

        # Masukkan data ke tabel View sesuai kolom pada database
        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id"],
                    buku["isbn"],
                    buku["title"],
                    buku["author"],
                    buku["category"],
                    buku["publication_year"],
                    buku["stock"],
                ),
            )

    def simpan_data(self):
        # Ambil nilai dari kolom input
        isbn = self.view.entry_isbn.get().strip() or None
        title = self.view.entry_judul.get().strip()
        author = self.view.entry_penulis.get().strip()
        category = self.view.entry_kategori.get().strip()
        publication_year = self.view.entry_tahun.get().strip() or None
        stock_input = self.view.entry_stok.get().strip()

        # Validasi kolom wajib
        if not title or not author or not category:
            messagebox.showwarning(
                "Peringatan",
                "Judul, penulis, dan kategori wajib diisi!",
            )
            return

        # Validasi tahun terbit jika diisi
        if publication_year is not None:
            try:
                publication_year = int(publication_year)
            except ValueError:
                messagebox.showwarning(
                    "Peringatan",
                    "Tahun terbit harus berupa angka.",
                )
                return

        # Gunakan 0 sebagai nilai stock jika input dikosongkan
        try:
            stock = int(stock_input) if stock_input else 0
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Stok harus berupa angka.",
            )
            return

        # Kirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(
            isbn,
            title,
            author,
            category,
            publication_year,
            stock,
        )

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")

            # Bersihkan kolom input
            self.view.entry_isbn.delete(0, "end")
            self.view.entry_judul.delete(0, "end")
            self.view.entry_penulis.delete(0, "end")
            self.view.entry_kategori.delete(0, "end")
            self.view.entry_tahun.delete(0, "end")
            self.view.entry_stok.delete(0, "end")

            # Muat ulang tabel agar menampilkan data terbaru
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menyimpan data.",
            )

    def run(self):
        self.view.mainloop()