import tkinter.messagebox as messagebox

from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role):
        self.user_role = (user_role or "").strip().lower()
        self.is_admin = self.user_role == "admin"

        self.model = BukuModel()
        self.view = BukuView()
        self.selected_id = None

        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_buku)

        # Non-admin hanya dapat melihat daftar buku.
        if not self.is_admin:
            self.view.btn_simpan.configure(
                state="disabled",
                text="Akses Terkunci (khusus Admin)",
            )
            self.view.btn_update.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")

            for entry in self._daftar_entry():
                entry.configure(state="disabled")

        self.muat_data_tabel()

    def _daftar_entry(self):
        return (
            self.view.entry_isbn,
            self.view.entry_judul,
            self.view.entry_penulis,
            self.view.entry_kategori,
            self.view.entry_tahun,
            self.view.entry_stok,
        )

    def _pastikan_admin(self):
        if not self.is_admin:
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk mengubah data buku.",
            )
            return False
        return True

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        for buku in self.model.get_all_buku():
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

    def pilih_buku(self, _event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return

        values = self.view.tabel.item(pilihan[0], "values")
        if not values:
            return

        self.selected_id = int(values[0])

        # Anggota dapat memilih baris untuk melihatnya, tetapi form tetap read-only.
        if not self.is_admin:
            return

        for entry, value in zip(self._daftar_entry(), values[1:]):
            entry.delete(0, "end")
            if value not in (None, ""):
                entry.insert(0, value)

    def _ambil_data_form(self):
        isbn = self.view.entry_isbn.get().strip() or None
        title = self.view.entry_judul.get().strip()
        author = self.view.entry_penulis.get().strip()
        category = self.view.entry_kategori.get().strip()
        year_text = self.view.entry_tahun.get().strip()
        stock_text = self.view.entry_stok.get().strip()

        if not title or not author or not category:
            messagebox.showwarning(
                "Peringatan",
                "Judul, penulis, dan kategori wajib diisi!",
            )
            return None

        try:
            publication_year = int(year_text) if year_text else None
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka.",
            )
            return None

        try:
            stock = int(stock_text) if stock_text else 0
            if stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Stok harus berupa angka nol atau lebih.",
            )
            return None

        return isbn, title, author, category, publication_year, stock

    def _bersihkan_form(self):
        for entry in self._daftar_entry():
            entry.delete(0, "end")

        self.selected_id = None
        for item in self.view.tabel.selection():
            self.view.tabel.selection_remove(item)

    def simpan_data(self):
        if not self._pastikan_admin():
            return

        data = self._ambil_data_form()
        if data is None:
            return

        if self.model.create_buku(*data):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self._bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menyimpan data.",
            )

    def perbarui_data(self):
        if not self._pastikan_admin():
            return

        if self.selected_id is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku pada tabel yang ingin diperbarui.",
            )
            return

        data = self._ambil_data_form()
        if data is None:
            return

        if self.model.update_buku(self.selected_id, *data):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self._bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data buku tidak berubah atau gagal diperbarui.",
            )

    def hapus_data(self):
        if not self._pastikan_admin():
            return

        if self.selected_id is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku pada tabel yang ingin dihapus.",
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus data buku ini?",
        )
        if not konfirmasi:
            return

        if self.model.delete_buku(self.selected_id):
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self._bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Data buku gagal dihapus.")

    def run(self):
        self.view.mainloop()
