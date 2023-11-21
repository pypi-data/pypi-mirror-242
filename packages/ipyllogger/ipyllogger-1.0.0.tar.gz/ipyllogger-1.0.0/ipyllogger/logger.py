import os


class AbstractLogger():

    base_path = 'logs'

    def __create_dir_if_not_exist(self, path:str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)

    def _write_log(self, filename:str, content:str, reset:bool) -> None:
        mode = 'w' if reset else 'a'

        self.__create_dir_if_not_exist(self.base_path)

        with open(f"{self.base_path}/{filename}", mode) as f:
            f.write(content)

    def _read_logs(self, filename:str) -> list[str]:
        try:
            with open(f"{self.base_path}/{filename}") as f:
                return f.readlines()
        except FileNotFoundError:

            self.__create_dir_if_not_exist(self.base_path)

            f = open(f"{self.base_path}/{filename}", 'w')
            f.close()
            return []
        

