import h5py
import numpy as np
from multiprocessing import shared_memory
from pathlib import Path
import time
import os


def load_to_shared_memory():
    path = Path("/media/koladik/HardDisk/data_rama/2025-12-23/mat")
    name = "Displace-X1.mat"
    full_path = path / name

    print(f"1. Загружаем данные из: {full_path}")

    # Загружаем данные из .mat
    with h5py.File(full_path, 'r') as f:
        t_data = f['D1/T'][:]
        x_data = f['D1/X'][:]

    print(f"2. Данные загружены: t {t_data.shape}, x {x_data.shape}")
    print(f"   Размер t в байтах: {t_data.nbytes}")
    print(f"   Размер x в байтах: {x_data.nbytes}")

    # Проверяем, нет ли уже блоков с такими именами
    for name in ['my_t_data', 'my_x_data']:
        try:
            old_shm = shared_memory.SharedMemory(name=name)
            old_shm.close()
            old_shm.unlink()
            print(f"   Удалили старый блок {name}")
        except FileNotFoundError:
            pass

    # Создаем shared memory блоки
    print("3. Создаем shared memory блоки...")
    shm_t = shared_memory.SharedMemory(create=True, size=t_data.nbytes, name='my_t_data')
    shm_x = shared_memory.SharedMemory(create=True, size=x_data.nbytes, name='my_x_data')

    print(f"4. Блоки созданы:")
    print(f"   t блок: {shm_t.name}, размер: {shm_t.size}")
    print(f"   x блок: {shm_x.name}, размер: {shm_x.size}")

    # Копируем данные
    t_shared = np.ndarray(t_data.shape, dtype=t_data.dtype, buffer=shm_t.buf)
    x_shared = np.ndarray(x_data.shape, dtype=x_data.dtype, buffer=shm_x.buf)
    t_shared[:] = t_data[:]
    x_shared[:] = x_data[:]

    print(f"5. Данные скопированы в shared memory")

    # Проверяем что файлы создались
    print("\n6. Проверяем /dev/shm/:")
    os.system("ls -la /dev/shm/ | grep my_")

    print("\n✅ Все готово! Скрипт остается запущенным...")
    print("🟢 Нажмите Ctrl+C для выхода")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🟡 Очистка shared memory...")
        shm_t.close()
        shm_t.unlink()
        shm_x.close()
        shm_x.unlink()
        print("✅ Память очищена")


if __name__ == "__main__":
    load_to_shared_memory()