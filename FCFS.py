import random
import pandas as pd
import numpy as np

def randomise():   #funkcja generująca losowe dane

  size = 100

  random.seed(60)   #ziarno losowości - pozwala nam na wygenerowanie losowych danych, będą one takie same przy każdym uruchomieniu programu, ale wciąż w gruncie rzeczy losowe

  burst_times = [random.randint(1, 30) for i in range(size)]   #tworzenie listy 'burst_time' odpowiadającej za przechowywanie czasów trwania danych procesów; ich ilość będzie zawsze równa wartości w zmiennej 'size'

  print("Burst times right after the draw: " + str(burst_times) + "\n")

  arrival_times = [random.randint(0, 30) for i in range(size)]   #tworzenie listy 'arrival_time' odpowiadającej za przechowywanie czasów przybycia danych procesów; ich ilość będzie zawsze równa wartości w zmiennej 'size'
  print("Arrival times right after the draw: " + str(arrival_times) + "\n")

  return arrival_times, burst_times, size   #zwracane są zapełnione listy 'arrival_time', 'burst_time' oraz zmienna 'size'

def FCFS(arrival_times, burst_times, size):   #funkcja przyjmująca listy 'arrival_time' i 'burst_time'; tu wykonywane są wszystkie obliczenia
  index = list(range(len(arrival_times)))   #lista pobierająca indeksy danych procesów wg 'arrival_time'

  arrival_copy = arrival_times.copy()   #lista przechowująca kopie danych czasów przybycia przed sortowaniem, właściwie tylko potrzebne do wyświetlania kolejności wykonywania procesów
  burst_copy = burst_times.copy()   #lista przechowująca kopie czasów trwania procesów przed sortowaniem, właściwie tylko potrzebne do wyświetlania kolejności wykonywania procesów
  index.sort(key=arrival_times.__getitem__)   #indeksy sortujemy rosnąco wg 'arrival_time'
  arrival_times[:] = [arrival_times[i] for i in index]   #elementy listy 'arrival_time' są sortowane wg danych indeksów listy 'index'
  burst_times[:] = [burst_times[i] for i in index]   #elementy listy 'burst_time' są sortowane wg danych indeksów listy 'index'; dzięki temu zapobiegamy mieszania się czasów przybycia i trwania procesów

  print("arr: " + str(arrival_times))
  print("burst: " + str(burst_times))

  index_table = index.copy()   #pobiera indeksy listy 'arrival_time' po sortowaniu

  completion_times = [0] * size   #tworzymy listę 'completion_times' i wypełniamy ją zerami, ilość taka jaka jest ilość procesów

  turnaround_times = [0] * size   #tworzymy listę 'turnaround_times' i wypełniamy ją zerami, ilość taka jaka jest ilość procesów

  waiting_times = [0] * size   #tworzymy listę 'waiting_times' i wypełniamy ją zerami, ilość taka jaka jest ilość procesów

  completion_times[0] = burst_times[0] + arrival_times[0]   #wypełniamy element o indeksie zero listy 'completion_times' czasem zakończenia się pierwszego procesu. Dla pierwszego procesu wchodzącego do procesora będzie to zawsze suma czasu jego przybycia i jego trwania
  waiting_times[0] = 0   #wypełniamy element o indeksie zero listy 'waiting_times' wartością zero - pierwszy proces nigdy nie czeka na swoje wykonanie, tylko w momencie rozpoczęcia się jego wykonywania po prostu się wykonuje

  for i in range(1, size):
    completion_times[i] = max(arrival_times[i], completion_times[i-1]) + burst_times[i]   #wypełniamy listę 'completion_times' czasami wykonania się kolejnych procesów - obliczamy dodając do siebie czas zakończenia się poprzedniego procesu i czas trwania obecnego procesu
    waiting_times[i] = completion_times[i] - arrival_times[i] - burst_times[i]   #wypełniamy listę 'waiting_times' czasami oczekiwania na wykonanie się danego procesu - obliczamy odejmując od czasu zakończenia się obecnego procesu jego czas przybycia i jego trwania

  for i in range(size):
    turnaround_times[i] = completion_times[i] - arrival_times[i]   #wypełniamy listę 'turnaround_times' czasami, jakie dane procesy spędzą w procesorze - obliczamy odejmując od czasu zakończenia się danego procesu jego czas przybycia


  return completion_times, turnaround_times, waiting_times, index_table, arrival_copy, burst_copy   #zwracane są struktury potrzebne do dalszych obliczeń i wyświetlania danych

def display(completion_times, turnaround_times, waiting_times, index_table, arrival_copy, burst_copy):   #funkcja wyświtlająca (i obliczająca jeszcze średnie czasy)
  average_turnaround_time = sum(turnaround_times) / len(turnaround_times)   #zmienna 'average_turnaround_time' przechowuje średni czas "spędzania" czasu procesów w procesorze
  print("Average Turnaround Time:")
  print(average_turnaround_time)
  print("\n")
  average_waiting_time = sum(waiting_times) / len(waiting_times)   #zmienna 'average_waiting_time' przechowuje średni czas oczekiwania procesu na swoje wykonanie
  print("Average Waiting Time: ")
  print(average_waiting_time)
  print("\n")
  print("Standard deviation of waiting times: ")
  print(str(np.std(waiting_times)))

  index_table = [j + 1 for j in index_table]   #zmieniam wyświetlanie ID procesów na numerację zaczynającą się od jedynki dla bardziej intuicyjnego zapisu

  tabela = pd.DataFrame({
    'Process ID': index_table,
    'Waiting Time': waiting_times,
    'Turnaround Time': turnaround_times,
    'Completion Time': completion_times
  })    #wykorzysując moduł pandas tworzę strukturę danych, która ułatwi wyświetlanie danych w formie tabeli

  print("\n Shown by the indices of processes")
  print(tabela)

  tabela.to_csv(r'FCFS_data.txt',header=True,index=None, sep='\t', mode='a')   #zapisuję do pliku dane w formie tabeli powyżej
  plik = open("FCFS_data.txt", "a")
  plik.write("\n")
  plik.write("ARRIVAL TIMES: " + str(arrival_copy) + "\n\n")
  plik.write("BURST TIMES: " + str(burst_copy) + "\n")
  plik.write("Average Turnaround Time: " + str(average_turnaround_time) + "\n")   #zapisuję także średni czas "spędzania" czasu procesów w procesorze
  plik.write("Average Waiting Time: " + str(average_waiting_time) + "\n")   #oraz średni czas oczekiwania na swoje wykonanie się
  plik.write("Standard deviation of waiting times: " + str(np.std(waiting_times)) + "\n")
  plik.write("Standard deviation of turnaround times: " + str(np.std(turnaround_times)) + "\n")
  plik.write("\n")
  plik.close()
  print("odchylenie standard czasow: ")
  std = np.std(waiting_times)
  print(std)
  print("odchylenie standard turnaround: ")
  std2 = np.std(turnaround_times)
  print(std2)

arrival_time, burst_time, size = randomise()
completion_times, turnaround_times, waiting_times, index_table, arrival_copy, burst_copy = FCFS(arrival_time, burst_time, size)
display(completion_times, turnaround_times, waiting_times, index_table, arrival_copy, burst_copy)
