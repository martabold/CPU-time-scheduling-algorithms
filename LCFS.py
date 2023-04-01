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

    return arrival_times, burst_times   #zwracane są zapełnione listy 'arrival_time' i 'burst_time'


def LCFS(arrival_times, burst_times):   #funkcja przyjmująca listy 'arrival_time' i 'burst_time'; tu wykonywane są wszystkie obliczenia
    index = list(range(len(arrival_times)))   #lista pobierająca indeksy danych procesów wg 'arrival_time'
    arrival_copy = arrival_times.copy()   #lista przechowująca kopie danych czasów przybycia przed sortowaniem, właściwie tylko potrzebne do wyświetlania kolejności wykonywania procesów
    burst_copy = burst_times.copy()   #lista przechowująca kopie czasów trwania procesów przed sortowaniem, właściwie tylko potrzebne do wyświetlania kolejności wykonywania procesów

    n = len(arrival_times)   #zmienna 'n' przechowująca ilość procesów

    index.sort(key=lambda i: (arrival_times[i], burst_times[i]))   #indeksy sortujemy rosnąco wg 'arrival_time' a potem wartości rosnąco wg 'burst_time', jeśli mamy więcej tych samych czasów przybycia
    arrival_times[:] = [arrival_times[i] for i in index]   #elementy listy 'arrival_time' są sortowane wg danych indeksów listy 'index'
    burst_times[:] = [burst_times[i] for i in index]   #elementy listy 'burst_time' są sortowane wg danych indeksów listy 'index'; dzięki temu zapobiegamy mieszania się czasów przybycia i trwania procesów

    completion_times = [0] * n   #tworzymy listę 'completion_times' i wypełniamy ją zerami, ilość taka jaka jest ilość procesów

    turnaround_times = [0] * n   #tworzymy listę 'turnaround_times' i wypełniamy ją zerami, ilość taka jaka jest ilość procesów

    waiting_times = [0] * n   #tworzymy listę 'waiting_times' i wypełniamy ją zerami, ilość taka jaka jest ilość procesów


    completion_times[0] = burst_times[0] + arrival_times[0]   #wypełniamy element o indeksie zero listy 'completion_times' czasem zakończenia się pierwszego procesu. Dla pierwszego procesu wchodzącego do procesora będzie to zawsze suma czasu jego przybycia i jego trwania
    waiting_times[0] = 0   #wypełniamy element o indeksie zero listy 'waiting_times' wartością zero - pierwszy proces nigdy nie czeka na swoje wykonanie, tylko w momencie rozpoczęcia się jego wykonywania po prostu się wykonuje
    turnaround_times[0] = completion_times[0] - arrival_times[0]   #wypełniamy element o indeskie zero listy 'turnaround_time' czasem "spędzanym" przez proces w procesorze. Jest to różnica jego  czasu zakończenia i czasu przybycia

    #index_table[0] = arrival_copy.index(arrival_times[0])   #wypełniamy listę 'index_table' o odpowiedni nr procesu

    poczekalnia = []   #tworzymy listę 'poczekalnia', będą tam przechowywane dane procesy, które czekają na swoje rozpoczęcie
    arrival_times.pop(0)   #usuwamy pierwszy element listy 'arrival_time', gdyż jest on już użyty do obliczeń
    burst_times.pop(0)   #usuwamy pierwszy element listy 'burst_times', gdyż jest on już użyty do obliczeń
    #n = len(arrival_times)   #aktualizujemy zawartość zmiennej 'n'
    n = n - 1

    i = 0    #zmienna pomocnicza do zasięgania indeksów list
    while n > 0:   #wykonuj dopóki nie skończą nam się procesy do przeanalizowania
        poczekalnia = sorted(item for item in arrival_times if item <= completion_times[i])  # and item > 0  #do poczekalni wpsiujemy te procesy (a dokładniej ich czas przybycia), które czekają na swoją kolej wykonania
        if len(poczekalnia) == 0:   #jeśli żaden proces nie czeka:

            completion_times[i + 1] = burst_times[i] + arrival_times[i]   #wypełniamy kolejny element listy 'completion_times' czasem zakończenia się tego procesu. Jest to suma czasu jego przybycia i jego trwania
            waiting_times[i + 1] = 0   #skoro ten proces nie czekał, to ma czas oczekiwania równy zero
            turnaround_times[i + 1] = completion_times[i + 1] - arrival_times[i]   #wypełniamy listę 'turnaround_times' czasem, jaki dany proces spędza w procesorze - obliczamy odejmując od czasu zakończenia się danego procesu jego czas przybycia
            arrival_times.pop(0)   #usuwamy dany analizowany proces z listy 'arrival_times'
            burst_times.pop(0)   #usuwamy dany analizowany proces z listy 'burst_times'

            i = i + 1   #zwiększamy zmienną pomocniczą
            n = n - 1   #zmniejszamy ilość procesów do analizowania
        else:   #jeśli jakieś procesy czekają

            g = max(j for j in poczekalnia)   #zmienna 'g' przechowuje analizowany obecnie proces, a dokładniej jego czas przybycia



            indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu = arrival_times.index(g)   #indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu przechowuje indeks czasu przybycia analizowanego procesu z listy 'arrival_times'

            completion_times[i + 1] = completion_times[i] + burst_times[indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu]   #wypełniamy kolejne miejsce w liście 'completion_times'; jest to suma czasu zakończenia się poprzedniego procesu i czasu trwania analizowanego procesu
            waiting_times[i + 1] = completion_times[i + 1] - arrival_times[indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu] - burst_times[indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu]   #wypełniamy kolejne miejsce w liście 'waiting_times'; obliczamy odejmując od czasu zakończenia się poprzedniego procesu czas przybycia i trwania analizowanego procesu
            turnaround_times[i + 1] = completion_times[i + 1] - arrival_times[indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu]   #wypełniamy kolejne miejsce w liście 'turnaround_times'; odejmujemy od czasu zakończenia się poprzedniego procesu czas przybycia analizowanego procesu

            arrival_times.pop(indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu)
            burst_times.pop(indeksNajwiekszaLiczbaPrzedSkonczeniemProcesu)
            poczekalnia.remove(max(poczekalnia))   #usuwamy największą daną z listy 'poczekalnia', jest to ta obecnie analizowana
            i = i + 1   #zwiększamy zmienną pomocniczą
            n = n - 1   #zmniejszamy ilość procesów do analizowania

    return completion_times, turnaround_times, waiting_times,arrival_copy, burst_copy   #zwracane są struktury potrzebne do dalszych obliczeń i wyświetlania danych


def display(completion_times, turnaround_times, waiting_times, arrival_copy, burst_copy):   #funkcja wyświtlająca (i obliczająca jeszcze średnie czasy)
    average_turnaround_time = sum(turnaround_times) / len(turnaround_times)   #zmienna 'average_turnaround_time' przechowuje średni czas "spędzania" czasu procesów w procesorze
    print("Average Turnaround Time:")
    print(average_turnaround_time)
    print("\n")

    average_waiting_time = sum(waiting_times) / len(waiting_times)   #zmienna 'average_waiting_time' przechowuje średni czas oczekiwania procesu na swoje wykonanie
    print("Average Waiting Time: ")
    print(average_waiting_time)
    print("\n")

    tabela = pd.DataFrame({
        #'Process ID': index_table,
        'Waiting Time': waiting_times,
        'Turnaround Time': turnaround_times,
        'Completion Time': completion_times
    })    #wykorzysując moduł pandas tworzę strukturę danych, która ułatwi wyświetlanie danych w formie tabeli

    print(tabela)

    tabela.to_csv(r'LCFS_data.txt', header=True, index=None, sep='\t', mode='a')   #zapisuję do pliku dane w formie tabeli powyżej
    plik = open("LCFS_data.txt", "a")
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


arrival_time, burst_time = randomise()
completion_times, turnaround_times, waiting_times, arrival_copy, burst_copy = LCFS(arrival_time, burst_time)
display(completion_times, turnaround_times, waiting_times, arrival_copy, burst_copy)

