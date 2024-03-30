import random
def randomID(len):
  choice="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890#$%!&"
  ret ="".join(random.choices(choice,k=len))
  return ret
def shuffle(list):
  l = len(list)
  todo = []
  ret = []
  for p in range(l):
    todo.append(p) #p th player have been done
    ret.append("-1")
  for i in range(l//2):
    get = random.sample(todo,2)
    #print(todo,get)
    todo.remove(get[0])
    todo.remove(get[1])
    ret[get[0]] = list[get[1]]
    ret[get[1]] = list[get[0]]
  if l%2:
    #print(ret,todo)
    last = []
    for i in range(l):
      if i != todo[0]:
        last.append(i)
    get = random.sample(last,1)
    ret[todo[0]] = ret[get[0]]
    ret[get[0]] = list[todo[0]]
  return ret