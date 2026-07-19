
import tkinter as tk
import time
import threading
import tkinter.messagebox
import winsound


class ReminderApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("吉大树洞提醒器")
        self.window.geometry("400x320")
        self.window.resizable(False, False)
        self.window.update_idletasks()
        w, h = self.window.winfo_width(), self.window.winfo_height()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"400x320+{(sw-w)//2}+{(sh-h)//2 - 100}")

        self.running = False
        self.remaining = 3600

        # 标题
        tk.Label(self.window, text="⏰ 吉大树洞提醒器",
                 font=("Microsoft YaHei", 18, "bold"), fg="#2E86AB"
                 ).pack(pady=(30, 5))

        tk.Label(self.window, text="点击开始，一小时后提醒你打开微信看树洞",
                 font=("Microsoft YaHei", 10), fg="#666"
                 ).pack(pady=(0, 20))

        # 倒计时数字
        self.timer_label = tk.Label(
            self.window, text="01:00:00",
            font=("Consolas", 36, "bold"), fg="#A23B72"
        )
        self.timer_label.pack(pady=10)

        # 进度条
        self.progress = tk.Canvas(
            self.window, width=300, height=12, bg="#E8E8E8", highlightthickness=0
        )
        self.progress.pack(pady=(10, 20))
        self.progress_bar = self.progress.create_rectangle(
            0, 0, 300, 12, fill="#6A994E", outline=""
        )

        # 按钮
        self.btn = tk.Button(
            self.window, text="开 始",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#2E86AB", fg="white", width=12,
            relief="flat", cursor="hand2", command=self.toggle
        )
        self.btn.pack(pady=10)

        self.status_label = tk.Label(
            self.window, text="就绪，等待开始...",
            font=("Microsoft YaHei", 9), fg="#999"
        )
        self.status_label.pack()

    def toggle(self):
        if not self.running:
            self.start()
        else:
            self.stop()

    def start(self):
        self.running, self.remaining = True, 3600
        self.btn.config(text="停 止", bg="#C73E1D")
        self.status_label.config(text="倒计时中... 去微信里用吉大树洞吧！", fg="#6A994E")
        threading.Thread(target=self.countdown, daemon=True).start()

    def stop(self):
        self.running = False
        self.btn.config(text="开 始", bg="#2E86AB", fg="white")
        self.status_label.config(text="已取消", fg="#999")
        self.timer_label.config(text="01:00:00")
        self.progress.coords(self.progress_bar, 0, 0, 300, 12)

    def countdown(self):
        while self.running and self.remaining > 0:
            h, m = divmod(self.remaining, 3600)
            m, s = divmod(m, 60)
            time_str = f"{h:02d}:{m:02d}:{s:02d}"
            self.window.after(0, self._update_display, time_str, self.remaining)
            time.sleep(1)
            self.remaining -= 1
        if self.running:
            self.window.after(0, self._times_up)

    def _update_display(self, time_str, remaining):
        self.timer_label.config(text=time_str)
        fill_width = int((remaining / 3600) * 300)
        self.progress.coords(self.progress_bar, 0, 0, fill_width, 12)

    def _times_up(self):
        self.running = False
        self.btn.config(text="开 始", bg="#2E86AB")
        self.status_label.config(text="时间到！快去打开微信看吉大树洞", fg="#C73E1D")
        self.timer_label.config(text="00:00:00")
        self.progress.coords(self.progress_bar, 0, 0, 0, 12)
        self.window.lift()
        self.window.focus_force()
        for _ in range(3):
            winsound.Beep(500, 800)
            time.sleep(0.3)
        tkinter.messagebox.showinfo(
            "⏰ 时间到！",
            "一小时到了！\n\n现在打开微信，进入吉大树洞看看吧。"
        )

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", lambda: (setattr(self, 'running', False), self.window.destroy()))
        self.window.mainloop()


if __name__ == "__main__":
    ReminderApp().run()
