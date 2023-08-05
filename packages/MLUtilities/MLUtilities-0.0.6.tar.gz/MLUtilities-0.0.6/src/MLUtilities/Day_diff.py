class Day_diff:
  """take the difference between two time columns"""
  def __init__(self,x,y):
         self.x = x # array of column names to encode
         self.y =y
  def take_diff(self):
      #a selects the number of days in the time difference
      a = (pd.to_timedelta(self.x-self.y).dt.days) .astype('float64')
      #convert the remainder in seconds to  days and add to a
      b = (pd.to_timedelta(self.x-self.y).dt.seconds)*1.1574074074074073e-05
      c  =  a+b 
      #convert date difference greater than 90 days to one group
      c  = [95 if i >90 else i for i in c  ]

      return c