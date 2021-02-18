# Start

# Get size of taget population from user input 
target_pop = int(input("Enter the population size: "))
# Get the life expectency of an individual from user input 
life_Exp = float(input("Enter life expectency: "))
# Get sample file name from user open and read 
samp_File = input ("Enter sample file name: ")
corona = open (samp_File, 'r')
# calculate the average age of infection from sample file 
l = corona.readlines()
samp_Corona = l
theSum = 0 
count = 0
for line in samp_Corona:
    line = line.strip()
    number = int(line)
    count += 1
    theSum += number 
average_Age = theSum / count

# calculate the base reproduction number (ro = life expectency / average age of infection from sample file)
ro = life_Exp / average_Age
# calculate herd immunity threshold (q = 1 - 1/ro)
q = 1 - (1 / ro)
# calculate the estimated number of doses (d = q * population size --from user input)
d = q * target_pop
# print 
#  Average age of  infection
print ("Average Age of Infection: ", str (round(average_Age, 2)))
#  ro
print ("Base Reproduction Number: ", str (round(ro, 9)))
#  q
print ("Herd Immunity Threshold: ", str (round(q, 8)))
#  d 
print ("Doses Required: ", str (round(d, 1)))
# END  


corona.close()


