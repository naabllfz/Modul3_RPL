from unittest.mock import MagicMock, patch

from models.buku_model import BukuModel


@patch("models.buku_model.Database")
def test_create_buku_berhasil(mock_database):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_database.return_value.get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    model = BukuModel()
    hasil = model.create_buku(
        None,
        "Buku Testing",
        "Penulis QA",
        "Umum",
        2026,
        0,
    )

    assert hasil is True
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


@patch("models.buku_model.Database")
def test_get_all_buku_berhasil(mock_database):
    data_buku = [
        {
            "id": 1,
            "isbn": "9780000000001",
            "title": "Buku Testing",
            "author": "Penulis QA",
            "category": "Umum",
            "publication_year": 2026,
            "stock": 3,
        }
    ]

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_database.return_value.get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = data_buku

    model = BukuModel()
    hasil = model.get_all_buku()

    assert hasil == data_buku
    mock_conn.cursor.assert_called_once_with(dictionary=True)
    mock_cursor.execute.assert_called_once_with("SELECT * FROM books")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
