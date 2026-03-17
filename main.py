import h5py
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from multiprocessing import shared_memory

def main():
    # Подключаемся к shared memory блокам
    print("Подключение к shared memory блокам...")
    existing_shm_t = shared_memory.SharedMemory(name='my_t_data')
    existing_shm_x = shared_memory.SharedMemory(name='my_x_data')

    print(f"✅ Подключились к блокам")
    print(f"   Размер блока t: {existing_shm_t.size} байт")
    print(f"   Размер блока x: {existing_shm_x.size} байт")

    # ВАЖНО: Создаем numpy массивы из shared memory
    # Форма (1, 5309182) как в loader.py
    t = np.ndarray((1, 5309182), dtype=np.float64, buffer=existing_shm_t.buf)
    x = np.ndarray((1, 5309182), dtype=np.float64, buffer=existing_shm_x.buf)


    # Создание фигуры и подграфика
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    # Отображение данных
    ax.plot(t, x, 'b-', linewidth=1.5)

    # Настройка графика
    ax.set_xlabel('Время (с)')
    ax.set_ylabel('Перемещение (мм)')
    ax.set_title('Перемещение D1/X от времени D1/T')
    ax.grid(True, alpha=0.3)

    # Отображение графика
    plt.tight_layout()
    plt.show()

def load_mat73_file(filepath):
    """Загрузка MATLAB v7.3 файла"""
    with h5py.File(filepath, 'r') as f:
        data_dict = {}

        def get_data(name, obj):
            if isinstance(obj, h5py.Dataset):
                # Загружаем данные и транспонируем для соответствия MATLAB
                data = obj[()]
                if len(data.shape) > 1:
                    data = data.T
                data_dict[name] = data

        f.visititems(get_data)
        return data_dict


if __name__ == "__main__":
    main()