import random

random.seed(42)

def generate_existing_data():
    random.seed(42)
    """
    Her sektör için sıcaklık ve hacim değerleri üretir.
    Returns:
        dict: {sector_id: (temp, vol)}
    """
    from Sector import sector_positions

    data = {}
    for sector in sector_positions:
        sector_id = str(sector["id"])
        temp = random.uniform(15, 85)
        vol = random.uniform(70, 300)
        data[sector_id] = (temp, vol)
    return data

def generate_simulated_data(temp=None, vol=None):
    random.seed(42)
    """
    Eğer parametre verilirse tüm sektörlere aynı temp ve vol gönderir,
    yoksa rastgele üretir.
    Returns:
        dict: {sector_id: (temp, vol)}
    """
    from Sector import sector_positions

    data = {}
    for sector in sector_positions:
        sector_id = str(sector["id"])
        if temp is not None and vol is not None:
            data[sector_id] = (temp, vol)
        else:
            t = random.uniform(15, 100)
            v = random.uniform(70, 300)
            data[sector_id] = (t, v)
    return data
