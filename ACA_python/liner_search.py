def call(temps):
    tot_temp = 0
    length_of_temps = 0
    for temp in temps:
        tot_temp += temp
        length_of_temps += 1
    average_temp = tot_temp / length_of_temps
    return average_temp


temps = [10, 20, 30, 40, 50]
print(call(temps))
