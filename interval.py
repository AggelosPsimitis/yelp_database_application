class Interval:
    def init(self,a,b):
	    self.a=a
	    self.b=b
    def isCorrectInterval(self):
        return self.a < self.b    
    def contains(self,number):
        return number < self.b and number > self.a
    def intersects(self,other):
        if self.b > other.a or self.a < other.b :
           return true
        else:
            return false
    def str(self):
        return '('+ self.a + ',' + self.b + ')'

import random

 def main():
     N = int(input('Give number of intervals'))
     interval_list = []
     count_cross_first_element= 0 
     count_countain_zero = 0
     for i in range(1,N,1):
         interval_list.append(Interval(random.uniform(-2, 3),random.uniform(-2,3)))
     for item in interval_list:
         if isCorrectInterval(item): 
             if intersects(item, interval_list(0)):
                 count_cross_first_element ++
             if contains(self,0) :
                 count_contain_zero++
     print(count_cross_zero)
     print(count_countain_zero)