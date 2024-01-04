import subprocess

def get_volume():
    try:
        result = subprocess.run(['amixer', 'get', 'Master'], capture_output=True, text=True)
        output = result.stdout
        volume_pos = output.find('[') + 1
        volume_end = output.find('%', volume_pos)
        volume = int(output[volume_pos:volume_end])
        return volume
    except Exception as e:
        print(f"Error al obtener el volumen: {e}")
        return None

def set_volume(volume):
    try:
        subprocess.run(['amixer', 'set', 'Master', f'{volume}%'])
        print(f'Volumen establecido en {volume}%')
    except Exception as e:
        print(f"Error al establecer el volumen: {e}")

# Obtener el volumen actual
current_volume = get_volume()
if current_volume is not None:
    print(f'Volumen actual: {current_volume}')

# Establecer un nuevo volumen (por ejemplo, 50%)
new_volume = 75
set_volume(new_volume)
