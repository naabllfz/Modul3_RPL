import tkinter.messagebox as messagebox

from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView


class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()
        self.selected_id = None

        self.view.btn_simpan.configure(command=self.simpan_anggota)
        self.view.btn_update.configure(command=self.perbarui_anggota)
        self.view.btn_hapus.configure(command=self.hapus_anggota)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_anggota)

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        for anggota in self.model.get_all_anggota():
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    anggota["id_anggota"],
                    anggota["nama"],
                    anggota["alamat"],
                ),
            )

    def pilih_anggota(self, _event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return

        values = self.view.tabel.item(pilihan[0], "values")
        if not values:
            return

        self.selected_id = int(values[0])
        self.view.entry_judul.delete(0, "end")
        self.view.entry_judul.insert(0, values[1])
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_penulis.insert(0, values[2])

    def _ambil_data_form(self):
        nama = self.view.entry_judul.get().strip()
        alamat = self.view.entry_penulis.get().strip()

        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Nama dan alamat anggota wajib diisi!",
            )
            return None

        return nama, alamat

    def _bersihkan_form(self):
        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.selected_id = None
        for item in self.view.tabel.selection():
            self.view.tabel.selection_remove(item)

    def simpan_anggota(self):
        data = self._ambil_data_form()
        if data is None:
            return

        if self.model.create_anggota(*data):
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self._bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menyimpan data anggota.",
            )

    def perbarui_anggota(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data anggota pada tabel yang ingin diperbarui.",
            )
            return

        data = self._ambil_data_form()
        if data is None:
            return

        if self.model.update_anggota(self.selected_id, *data):
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self._bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data anggota tidak berubah atau gagal diperbarui.",
            )

    def hapus_anggota(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data anggota pada tabel yang ingin dihapus.",
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus data anggota ini?",
        )
        if not konfirmasi:
            return

        if self.model.delete_anggota(self.selected_id):
            messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
            self._bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Data anggota gagal dihapus.")

    def run(self):
        self.view.mainloop()
