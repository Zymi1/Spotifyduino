import time
import serial

#incoming_string = "Kuki : Wakacyjne pierdolenie twojej starej na basenie"
incoming_string = "Kuki : Wakacyjne"
old_string = "Miles Davis : Freddie Freeloader"

def converter(list):
    string_to_send = ""
    for elements in range(0,16):
        string_to_send += dane[elements]
    return string_to_send

while True:
    first_print = 0
    if (old_string == incoming_string):
        string_for_slicing_original = old_string
        string_for_slicing = old_string
        dane_original = list(string_for_slicing_original)
        dane = list(string_for_slicing)
        for el in range(0,4):
            dane.append(" ")
            dane_original.append(" ")
        dlugosc = ((len(dane_original)-17))
        if first_print == 0:
            print(converter(dane[0:16]))
            first_print + 1
        for n in range(len(dane)):
            if old_string != incoming_string:
                break
            if n >= dlugosc + 1:
                break
            dane.pop(0)
            dane.append(dane[n])
            print(dane[0:16])
            time.sleep(0.2)
            #arduino.write(bytes(str(string), 'utf-8'))
            #time.sleep(5)
            if n >= dlugosc:
                for x in range(16,len(dane_original)):
                    dane.pop()
                for m in range(0,16):
                    if old_string != incoming_string:
                        break
                    dane.pop(0)
                    dane.append(dane_original[m])
                    print(dane[0:16])
                    time.sleep(0.2)
                    if m == 15:
                        break

    else:
        old_string = incoming_string