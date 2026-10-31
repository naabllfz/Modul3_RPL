from unittest.mock import MagicMock, patch

from models.buku_model import BukuModel


@patch("models.buku_model.Database")
def test_create_buku_berhasil(mock_database):
    # Siapkan koneksi dan cursor tiruan agar tes tidak mengakses database asli
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_database.return_value.get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Inisialisasi Model
    model = BukuModel()

    # Jalankan fungsi dengan urutan argumen:
    # isbn, title, author, category, publication_year, stock
    hasil = model.create_buku(
        None,
        "Buku Testing",
        "Penulis QA",
        "Umum",
        2026,
        0,
    )

    # Pastikan penyimpanan berhasil
    assert hasil is True

    # Pastikan query dijalankan dan perubahan di-commit
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()