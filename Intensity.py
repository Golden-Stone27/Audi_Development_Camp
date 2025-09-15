from Simulate import train_and_predict
from Sector import sector_positions

def get_intensity(temp, vol, sector_id=None):
    water_consumption = train_and_predict(temp, vol)
    # divider for normalizing (example 400)
    base_intensity = water_consumption / 450

    if sector_id is not None:
        sector = next((s for s in sector_positions if str(s["id"]) == str(sector_id)), None)
        factor = sector.get("factor", 1.0) if sector else 1.0
    else:
        factor = 1.0

    adjusted_intensity = float(base_intensity * factor)
    return adjusted_intensity
