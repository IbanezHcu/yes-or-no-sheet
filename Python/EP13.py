#โปรแกรมคำนวนค่า BMI (ดัชนีมวลกาย)
#BMI = น้ำหนัก (kg) / ส่วนสูง * ส่วนสูง (m)

#input / convert to integer
weight = int (input(" กรุณาป้อนน้ำหนักของคุณ (kg) : "))
high = int(input(" ป้อนส่วนสูงของคุณ (cm) : ")) /100

#Process
#cm => m
#high = high/100 #high /=100
#Calulate BMI
#BMI = weight/(high*high) #(high**2)

#output
print("BMI = " ,weight/(high*high)) #(high**2))

#print (BMI)