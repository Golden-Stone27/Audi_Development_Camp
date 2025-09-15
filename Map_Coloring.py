import random
from PIL import Image, ImageDraw
from Simulate import train_and_predict
from Sector import sector_positions
from Intensity import get_intensity
from PIL import ImageFont
from global_vars import show_water_var


font = ImageFont.truetype("arial.ttf", 14)  # 16 istediğin kadar büyütülebilir
random.seed(42)

def get_simulated_intensities(temp, vol):
    from Intensity import get_intensity
    from Sector import sector_positions

    simulated_data = {}

    for sector in sector_positions:
        sector_id = str(sector["id"])
        intensity = get_intensity(temp, vol, sector_id)
        simulated_data[sector_id] = intensity

    return simulated_data

from global_vars import existing_intensity_data

def get_existing_intensities():
    return existing_intensity_data



def Existing_coloring(existing_data, show_water):
    image = Image.open("map.jpg").convert("RGBA")
    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for sector in sector_positions:
        sid = str(sector["id"])
        x, y, radius = sector["x"], sector["y"], sector["radius"]

        temp, vol = existing_data.get(sid, (None, None))
        if temp is None or vol is None:
            continue

        intensity = get_intensity(temp, vol, sector)
        water_consumption = train_and_predict(temp, vol)

        r = int(255 * intensity)
        g = int(255 * (1 - intensity))
        color = (r, g, 0)
        opacity = 100

        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color + (opacity,))

        if show_water and water_consumption is not None:
            draw.text((x - radius + 1, y + radius + 3), f"{water_consumption:.1f} L", fill="black", font=font)

    combined = Image.alpha_composite(image, overlay)
    combined.save("output_existing.png")
    combined.show()

def Simulated_Coloring(simulated_data, show_water):
    image = Image.open("map.jpg").convert("RGBA")
    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for sector in sector_positions:
        sid = str(sector["id"])
        factor = float(sector["factor"])
        x, y, radius = sector["x"], sector["y"], sector["radius"]

        temp, vol = simulated_data.get(sid, (None, None))
        if temp is None or vol is None:
            continue

        intensity = get_intensity(temp, vol, sid)
        water_consumption = train_and_predict(temp, vol) * factor
        print(f"Sector_id: {sid}  Temp: {temp}  Volume: {vol} Intensity: {intensity}")
        r = int(255 * intensity)
        g = int(255 * (1 - intensity))
        color = (r, g, 0)
        opacity = 100

        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color + (opacity,))

        if show_water and water_consumption is not None:
            draw.text((x - radius + 1, y + radius + 4), f"{water_consumption:.1f} L", fill="black", font=font)

    combined = Image.alpha_composite(image, overlay)
    combined.save("output_simulated_all.png")
    combined.show()

'''
def draw_single_sector(intensity, sector_id, water_consumption, show_water=False, volume=None):
    image = Image.open("map.jpg").convert("RGBA")

    sector = next((s for s in sector_positions if str(s["id"]) == str(sector_id)), None)
    if sector is None:
        print(f"Sektor ID {sector_id} could not be found.")
        return

    x = sector["x"]
    y = sector["y"]
    radius = sector["radius"]

    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    r = int(255 * intensity)
    g = int(255 * (1 - intensity))
    fill = (r, g, 0, 100)

    # Daireyi çiz
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=fill)

    # Su miktarını dairenin altına yaz
    if water_consumption and show_water and volume is not None:
        water_text = f"{water_consumption:.1f} L"
        draw.text((x - radius, y + radius + 3), water_text, fill="black", font=font)

    combined = Image.alpha_composite(image, overlay)
    combined.save(f"single_sector_{sector_id}.png")
    combined.show()

    print(f"Sector {sector_id} drawn at ({x},{y}) with intensity {intensity:.2f}")
'''
def draw_multiple_sectors(sector_data_list, show_water=False):
    image = Image.open("map.jpg").convert("RGBA")
    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for data in sector_data_list:
        sector_id = data["id"]
        intensity = data["intensity"]
        water = data["water"]
        volume = data["volume"]
        temp = data["Temp"]


        print(f"Sector_id: {sector_id}  Temp: {temp}  Volume: {volume} Intensity:{intensity}")

        sector = next((s for s in sector_positions if str(s["id"]) == str(sector_id)), None)
        if sector is None:
            continue

        x, y, radius = sector["x"], sector["y"], sector["radius"]
        r = int(255 * intensity)
        g = int(255 * (1 - intensity))
        fill = (r, g, 0, 100)

        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=fill)

        if show_water and water is not None:
            text = f"{water:.1f} L"
            draw.text((x - radius, y + radius + 3), text, fill="black", font=font)

    combined = Image.alpha_composite(image, overlay)
    combined.save("selected_sectors.png")
    combined.show()


def draw_comparison_map(differences):
    """
    differences: {sector_id: difference value}
    Pozitif farklar kırmızı tonları, negatif farklar mavi tonları ile gösterilsin.
    """
    image = Image.open("map.jpg").convert("RGBA")
    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    max_diff = max(abs(diff) for diff in differences.values()) or 1  # Sıfıra bölme önlemi

    for sector in sector_positions:
        sid = str(sector["id"])
        diff = differences.get(sid, 0)

        x, y, radius = sector["x"], sector["y"], sector["radius"]

        # Normalize fark -1..1 aralığına çekelim
        norm_diff = diff / max_diff

        if norm_diff > 0:
            # Pozitif fark: kırmızı tonları (0,0,0) -> (255,0,0)
            r = int(255 * norm_diff)
            g = 0
            b = 0
        else:
            # Negatif fark: mavi tonları (0,0,0) -> (0,0,255)
            r = 0
            g = 0
            b = int(255 * abs(norm_diff))

        opacity = 150
        color = (r, g, b, opacity)

        draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)

        # Fark değerini yazdır
        text = f"{diff:+.2f}"
        draw.text((x - radius, y + radius + 3), text, fill="black", font=font)

    combined = Image.alpha_composite(image, overlay)
    combined.save("comparison_map.png")
    combined.show()