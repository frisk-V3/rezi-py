import tkinter as tk
import csv
from datetime import datetime

cart = []  # (name, price)

# 商品マスタ読み込み
def load_items():
    items = []
    with open("items.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for name, price in reader:
            items.append((name, int(price)))
    return items

items = load_items()

def add_item(name, price):
    cart.append((name, price))
    listbox.insert(tk.END, f"{name} - {price}円")
    update_total()

def update_total():
    total = sum(p for _, p in cart)
    label_total.config(text=f"合計: {total}円")

def checkout():
    if not cart:
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(p for _, p in cart)

    # 売上履歴に保存
    with open("sales.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for name, price in cart:
            writer.writerow([now, name, price])

    # レシート生成（テキスト）
    with open("receipt.txt", "w", encoding="utf-8") as f:
        f.write("=== レシート ===\n")
        f.write(f"日時: {now}\n\n")
        for name, price in cart:
            f.write(f"{name}  {price}円\n")
        f.write("\n")
        f.write(f"合計: {total}円\n")
        f.write("================\n")
        f.write("※ PDF化は印刷 → PDF を選択\n")

    cart.clear()
    listbox.delete(0, tk.END)
    update_total()

def show_sales():
    win = tk.Toplevel(root)
    win.title("売上履歴")

    lb = tk.Listbox(win, width=40)
    lb.pack()

    with open("sales.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            lb.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}円")

root = tk.Tk()
root.title("POSレジ")

# 商品ボタン
for name, price in items:
    tk.Button(root, text=f"{name} ({price}円)",
              command=lambda n=name, p=price: add_item(n, p)).pack()

listbox = tk.Listbox(root, width=30)
listbox.pack()

label_total = tk.Label(root, text="合計: 0円")
label_total.pack()

tk.Button(root, text="会計（レシート生成）", command=checkout).pack()
tk.Button(root, text="売上履歴を見る", command=show_sales).pack()

root.mainloop()
