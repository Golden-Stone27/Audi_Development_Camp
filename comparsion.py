from Simulate import train_and_predict
from Intensity import get_intensity
from Sector import sector_positions

def calculate_differences(existing_data, simulated_data):
    """
    existing_data ve simulated_data: {sector_id: intensity}
    Return: {sector_id: difference = simulated - existing}
    """
    differences = {}
    for sector in sector_positions:
        sid = str(sector["id"])
        existing_intensity = existing_data.get(sid, 0)
        simulated_intensity = simulated_data.get(sid, 0)
        differences[sid] = simulated_intensity - existing_intensity
    return differences
