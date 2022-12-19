import queue
from threading import Thread
import subprocess
import time


class Ping_threads():
    def __init__(self, lista_ips: list, num_threads=50) -> None:
        """Executa ping simultâneo em múltiplos endereços, usando threads

        Args:
            lista_ips (list): Lista com endereços IP a \
                serem verificados se respondem
            num_threads (int, optional): Quantidade de \
                threads a serem usadas. Defaults to 30.
        """
        inicio = time.time()

        self.fila_ips = queue.Queue()
        self.fila_respostas = queue.Queue()

        self.executar_threads(num_threads)
        self.preencher_filas_ips(self.fila_ips, lista_ips)
        self.fila_ips.join()  # aguarda fila terminar
        self.respostas = self.extrair_resultado(self.fila_respostas)
        fim = time.time()
        print(fim - inicio)

    def executar_ping(self):
        """Cria subprocesso que executa o ping pelo sistema operacional
        Usa como base a variável self.fila_ips
        Preenche self.fila_respostas com o resultado
        """
        while True:
            ip = self.fila_ips.get()
            args = f"ping -n 1 -w 1 {ip}"
            proc = subprocess.Popen(args,
                                    shell=False,
                                    stdout=subprocess.PIPE)
            # obtém a saída do comando, mas não usa
            stdout, stderr = proc.communicate()

            # preenche a fila de respostas com um dicionário do resultado:
            # "ip": endereço verificado,
            # "responde": True se responde, False se houve erro
            if proc.wait() == 0:
                self.fila_respostas.put({"ip": ip, "responde": True})
            else:
                self.fila_respostas.put({"ip": ip, "responde": False})
            self.fila_ips.task_done()

    def preencher_filas_ips(self, fila_ips: queue.Queue, lista_ips: list):
        """Preenche a fila com valores dos IPs a serem verificados

        Args:
            fila_ips (queue.Queue): Objeto fila que guarda os valores
            lista_ips (list): lista de IPs recebida pelo objeto
        """
        for x in lista_ips:
            self.fila_ips.put(x)

    def executar_threads(self, num_threads: int) -> None:
        """Executa o método executar_ping usando threads
        Args:
            num_threads (int): Número de threads a ser usada para processo
        """
        for x in range(1, num_threads):
            trabalhador = Thread(target=self.executar_ping)
            trabalhador.setDaemon(True)
            trabalhador.start()

    def extrair_resultado(self, fila_respostas: queue.Queue) -> list:
        """Obtém a partir da fila de respostas
        a lista dos dicionários com o resultado do processamento
        Args:
            fila_respostas (queue.Queue): Fila com informações obtidas dos pings

        Returns:
            list: lista de dicionários com IP(str) e resposta (bool)
        """
        lista_respostas = []
        while True:
            try:
                # obtém valor sem aguardar execução
                resposta = fila_respostas.get_nowait()
                lista_respostas.append(resposta)
            except queue.Empty:
                break  # quebra o laço quando lista fica vazia
        return lista_respostas


if __name__ == "__main__":
    lista_ips = []
    for x in range(1, 254):
        ip = f"192.168.0.{x}"
        lista_ips.append(ip)
    ping_thread = Ping_threads(lista_ips)
    print(ping_thread.respostas)
