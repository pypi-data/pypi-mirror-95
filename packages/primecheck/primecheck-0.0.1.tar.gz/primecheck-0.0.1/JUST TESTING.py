def prime_check(x):
	i:int=1
	to_check=[]
	while i < (round(x**(1/2))+3):
		to_check.append(i)
		i+=1
	for i in to_check:
		if x%i==0 and i!=1:
			return False
	return True

sting=prime_check(1234567890123)
print(str(sting))