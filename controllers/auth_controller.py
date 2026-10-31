import tkinter.messagebox as messagebox

from controllers.buku_controller import BukuController
from models.user_model import UserModel
from views.login_view import LoginView


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.buku_controller = None

        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Peringatan",
                "Username dan password wajib diisi!",
                parent=self.view,
            )
            return

        user = self.model.autentikasi(username, password)

        if not user:
            messagebox.showerror(
                "Login Gagal",
                "Username atau password salah.",
                parent=self.view,
            )
            return

        messagebox.showinfo(
            "Login Berhasil",
            f"Selamat datang, {user['username']} ({user['role']})!",
            parent=self.view,
        )

        self.view.withdraw()
        self.buku_controller = BukuController(
            master=self.view,
            user_role=user["role"],
            on_logout=self.kembali_ke_login,
        )

    def kembali_ke_login(self):
        self.buku_controller = None
        self.view.entry_username.delete(0, "end")
        self.view.entry_password.delete(0, "end")
        self.view.deiconify()
        self.view.lift()
        self.view.focus_force()

    def run(self):
        self.view.mainloop()