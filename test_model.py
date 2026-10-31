from models.buku_model import BukuModel
from models.anggota_model import AnggotaModel


def uji_buku():
    model = BukuModel()

    print("=== Uji Create Buku ===")
    if model.create_buku("Buku Uji CRUD", "Penulis Uji", 2024):
        print("Buku berhasil ditambahkan.")
    else:
        print("Buku gagal ditambahkan.")

    print("\n=== Daftar Buku ===")
    daftar_buku = model.get_all_buku()

    for buku in daftar_buku:
        print(
            f"[{buku['id_buku']}] {buku['judul']} - "
            f"{buku['penulis']} ({buku['tahun_terbit']})"
        )

    id_buku = int(input("\nMasukkan id_buku untuk diuji: "))

    print("\n=== Uji Update Buku ===")
    berhasil_update = model.update_buku(
        id_buku,
        "Judul Setelah Update",
        "Penulis Uji",
        2025,
    )

    if berhasil_update:
        print("Data buku berhasil diperbarui.")
    else:
        print("Data buku tidak ditemukan atau gagal diperbarui.")

    print("\n=== Uji Delete Buku ===")
    konfirmasi = input(
        f"Yakin menghapus buku dengan id {id_buku}? (y/t): "
    ).lower()

    if konfirmasi == "y":
        if model.delete_buku(id_buku):
            print("Data buku berhasil dihapus.")
        else:
            print("Data buku tidak ditemukan atau gagal dihapus.")
    else:
        print("Penghapusan dibatalkan.")


def uji_anggota():
    model = AnggotaModel()

    print("\n=== Uji Create Anggota ===")
    nama = input("Masukkan nama anggota: ")
    alamat = input("Masukkan alamat anggota: ")

    if model.create_anggota(nama, alamat):
        print("Anggota berhasil ditambahkan.")
    else:
        print("Anggota gagal ditambahkan.")

    print("\n=== Daftar Anggota ===")
    daftar_anggota = model.get_all_anggota()

    for anggota in daftar_anggota:
        print(
            f"[{anggota['id_anggota']}] "
            f"{anggota['nama']} - {anggota['alamat']}"
        )


if __name__ == "__main__":
    uji_buku()
    uji_anggota()