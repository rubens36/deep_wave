#AUTOGENERATED! DO NOT EDIT! File to edit: dev/00_preprocessing.ipynb (unless otherwise specified).

__all__ = ['TimeSerie']

#Cell
class TimeSerie:
    "Estructura de datos que almacena las mediciones en una estacion."

    @staticmethod
    def __process_time(time):
        match = re.match(r"(?P<val>\d+)(?P<smh>[smh]*)$", time, re.I)
        assert match, "Formato incorrecto de tamaño de ventana o paso."

        result = int(match.group("val"))
        if match.group("smh").lower() == "m":
            result *= 60
        elif match.group("smh").lower() == "h":
            result *= 60*60
        return result


    def __init__(self, window_size:str="2m", step:str="30s", freq:int=50):
        "El formato de `window_size` y `step` es \d+[smh]"
        "`window_size` representa el tamaño de tiempo en que sera cortada la serie de tiempo"
        "`step` representa el tamaño de paso que se utiliza al cortar la serie de tiempo"
        "`freq` es la frecuencia en Hz que tienen las mediciones"

        self.window_size = self.__process_time(window_size)
        self.step = self.__process_time(step)

        assert type(freq) is int, "La frecuencia debe ser un entero."
        assert freq > 0 and freq <= 500, "La frecuencia debe definirse entre 1 y 500 Hz"
        self.freq = freq

    @staticmethod
    def load_data_one_file(file_path, station="B2DF", channel="001"):
        """
        Busca en el camino del archivo pasado por parametros y
        retorna un diccionario con la fecha de inicio y termino,
        ademas de los datos correspondientes a la estacion y el canal pasados por parametros.
        """
        st = read(str(file_path))
        for tr in st:
            if tr.stats.station == station and tr.stats.channel == channel:
                return {"start": tr.stats.starttime, "end": tr.stats.endtime, "data": tr.data}

    @staticmethod
    def load_data_list(list_file_path, station="B2DF", channel="001"):
        """
        Busca en cada camino de archivo de la lista pasado por parametros y
        retorna una lista de diccionarios con las fecha de inicio y termino,
        ademas de los datos correspondientes a la estacion y el canal pasados por parametros.
        """
        data = [
                 TimeSerie.load_data_one_file(file_path, station, channel) \
                 for file_path in list_file_path \
                 if not file_path.is_dir()
               ]
        return data

    @staticmethod
    def load_data_folder(folder_path, station="B2DF", channel="001"):
        """
        Busca en cada archivo miniseed del directorio pasado por parametros y
        retorna una lista de diccionarios con las fecha de inicio y termino,
        ademas de los datos correspondientes a la estacion y el canal pasados por parametros.
        """
        data = TimeSerie.load_data_list(folder_path.glob("**/*"), station, channel)
        return data

    def __repr__(self):
        return f"window_size {self.window_size}\nstep {self.step}\nfreq {self.freq}"

    def __str__(self):
        return f"window_size {self.window_size}\nstep {self.step}\nfreq {self.freq}"