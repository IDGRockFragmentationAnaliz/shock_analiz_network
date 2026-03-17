import h5py
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

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


def main():
    path = Path("/media/koladik/HardDisk/data_rama/2025-12-23/mat")
    name = "Displace-X1.mat"
    path_file = path / name

    dict = load_mat73_file(path_file)
    print(dict.keys())
    t = dict['D1/T']
    x = dict['D1/X']

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


if __name__ == "__main__":
    main()