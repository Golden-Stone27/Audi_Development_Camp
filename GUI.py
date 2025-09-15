import tkinter as tk
from Map_Coloring import Existing_coloring, Simulated_Coloring, draw_multiple_sectors
from Intensity import get_intensity
from PIL import Image, ImageTk
from Simulate import train_and_predict
import global_vars
from Sector import sector_positions
from tkinter import Toplevel, Checkbutton, IntVar

selected_sectors = {}


root = tk.Tk()
global_vars.show_water_var = tk.BooleanVar()
root.title("Water Intensity Simulator")
root.geometry("800x600")  # Başlangıç boyutu
root.iconbitmap("audi.ico")

# Sütun genişlemesi için root ayarı
root.grid_columnconfigure(0, weight=0)  # label sütunu sabit kalsın istersen
root.grid_columnconfigure(1, weight=1)  # input ve butonların olduğu sütun tam genişlesin

# Temperature input
tk.Label(root, text="Temperature (°C):").grid(row=0, column=0, padx=10, pady=5)
temperature_entry = tk.Entry(root)
temperature_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

# Volume input
tk.Label(root, text="Volume (L):").grid(row=1, column=0, padx=10, pady=5)
volume_entry = tk.Entry(root)
volume_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

'''
# Sector ID input
tk.Label(root, text="Sector ID (1–78 or A–H):").grid(row=2, column=0, padx=10, pady=5)


sector_entry = tk.Entry(root)
sector_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

def on_simulate_single():
    try:
        temp = float(temperature_entry.get())
        vol = float(volume_entry.get())
        sector_id = sector_entry.get().strip()
        water_consumption = train_and_predict(temp, vol)
        intensity = get_intensity(temp, vol, sector_id)

        print(f"Simulated Sector {sector_id}: intensity={intensity:.2f}, Water Consumption={water_consumption:.2f}")

        show_water = show_water_var.get()
        draw_single_sector(intensity, sector_id, water_consumption, show_water, vol)

    except Exception as e:
        print("Hata:", e)
'''

import data_generator

def draw_existing_data():
    existing_data = data_generator.generate_existing_data()
    show_water = show_water_var.get()
    Existing_coloring(existing_data, show_water)

def draw_simulated_all():
    # İstersen kullanıcıdan al veya sabit değer ver
    temp_str = temperature_entry.get()
    vol_str = volume_entry.get()
    try:
        temp = float(temp_str)
        vol = float(vol_str)
    except:
        temp, vol = None, None

    simulated_data = data_generator.generate_simulated_data(temp, vol)
    show_water = show_water_var.get()
    Simulated_Coloring(simulated_data, show_water)

def open_sector_selector():

    selector_win = Toplevel(root)
    selector_win.title("Select Sectors to Simulate")
    selector_win.iconbitmap("audi.ico")
    row = 0
    for sector in sector_positions:
        sid = str(sector["id"])
        if sid not in selected_sectors:
            selected_sectors[sid] = IntVar()

        chk = Checkbutton(selector_win, text=sid, variable=selected_sectors[sid])
        chk.grid(row=row//8, column=row % 8, sticky="w", padx=3, pady=2)
        row += 1

def simulate_selected_sectors():
    from Sector import sector_positions
    try:
        temp_str = temperature_entry.get().strip()
        vol_str = volume_entry.get().strip()

        if not temp_str or not vol_str:
            print("Lütfen sıcaklık ve hacim değerlerini giriniz!")
            return

        temp = float(temp_str)
        vol = float(vol_str)
        show_water = show_water_var.get()

        sector_data_list = []

        selected = [sid for sid, var in selected_sectors.items() if var.get()]
        print(f"Seçilen sektörler: {selected}")

        if not selected:
            print("Lütfen en az bir sektör seçiniz.")
            return

        for sid in selected:
            # İlgili sektörü bul
            sector = next((s for s in sector_positions if str(s["id"]) == str(sid)), None)
            if not sector:
                print(f"Sektor bulunamadı: {sid}")
                continue

            factor = sector.get("factor", 1.0)  # factor değeri yoksa 1.0 varsay
            intensity = get_intensity(temp, vol, sid)
            water = train_and_predict(temp, vol) * factor

            sector_data_list.append({
                "id": sid,
                "intensity": intensity,
                "water": water,
                "volume": vol,
                "Temp": temp,
            })

        draw_multiple_sectors(sector_data_list, show_water)

    except Exception as e:
        print("Hata:", e)


import comparsion
from Intensity import get_intensity
from global_vars import existing_intensity_data

def on_compare():
    # Önce existing intensities al
    existing_data = existing_intensity_data  # {sector_id: intensity}

    # Simulated için sıcaklık ve hacim al
    try:
        temp = float(temperature_entry.get())
        vol = float(volume_entry.get())
    except ValueError:
        print("Geçerli sıcaklık ve hacim giriniz!")
        return

    # Simulated intensity hesapla
    simulated_data = {}
    for sector in sector_positions:
        sid = str(sector["id"])
        simulated_data[sid] = get_intensity(temp, vol, sid)

    # Farkları hesapla
    differences = (comparsion.calculate_differences(existing_data, simulated_data))

    # Harita üzerinde çizdir
    import Map_Coloring
    Map_Coloring.draw_comparison_map(differences)




'''
# Simulate single sector
btn_single = tk.Button(root, text="Simulate Single Sector", command=on_simulate_single)
btn_single.grid(row=4, column=0, columnspan=2, pady=5, sticky='ew')
'''
# Show existing data
btn_existing = tk.Button(root, text="Show Existing Data", command=draw_existing_data)
btn_existing.grid(row=7, column=0, columnspan=2, pady=5, sticky='ew')


# Simulate all sectors
simulate_all_button = tk.Button(root, text="Simulate All Sectors", command=draw_simulated_all)
simulate_all_button.grid(row=8, column=0, columnspan=2, pady=10, sticky='ew')


# Alt kısım için kırmızı arka planlı Frame
bottom_frame = tk.Frame(root, bg="red", height=80)
bottom_frame.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(50, 0))

# row 7 için satır yüksekliğini sabitle (minimum 80 piksel)
root.grid_rowconfigure(9, minsize=80)

# Audi logosunu yükle ve küçült
audi_img = Image.open("audi_logo.png")  # audi_logo.png dosyasını aynı klasöre koymalısın
audi_img = audi_img.resize((70, 70), Image.Resampling.LANCZOS)
audi_photo = ImageTk.PhotoImage(audi_img)

# Logo için Label
logo_label = tk.Label(bottom_frame, image=audi_photo, bg="red")
logo_label.pack(side="left", padx=10, pady=5)

# Yazı Label
text_label = tk.Label(bottom_frame, text="Audi Hungaria", fg="white", bg="red", font=("Arial", 24, "bold"))
text_label.pack(side="left", padx=10)

logo_label.pack(side="left", padx=10, pady=15)
text_label.pack(side="left", padx=10, pady=15)

# Checkbutton için Tkinter değişkeni tanımla
show_water_var = tk.BooleanVar()

# Kullanıcı seçebilsin diye GUI'ye ekle
check_water = tk.Checkbutton(root, text="Show Water Amount", variable=show_water_var)
check_water.grid(row=9, column=0, columnspan=2, pady=5, sticky="w")

# Sektör seçim butonu
btn_select_sectors = tk.Button(root, text="Select Sectors", command=open_sector_selector)
btn_select_sectors.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

# Seçilen sektörleri simüle et butonu
btn_simulate_selected = tk.Button(root, text="Simulate Selected Sectors", command=simulate_selected_sectors)
btn_simulate_selected.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

btn_compare = tk.Button(root, text="Compare Simulated vs Existing", command=on_compare)
btn_compare.grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")


root.mainloop()
