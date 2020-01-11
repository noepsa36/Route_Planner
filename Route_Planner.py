import math

class Path:
    def __init__(self,path,remaining,value = 0):
        self.path = path
        self.value = value
        self.remaining = remaining
    
    def __repr__(self):
        return "(" + str(self.value) + ",(" + str(self.path) + "))"

    def __le__(self,other):
        return (self.value + self.remaining) <= (other.value + other.remaining)

    def __ge__(self,other):
        return (self.value + self.remaining) >= (other.value + other.remaining)
    
    def __eq__(self,other):
        return (self.value + self.remaining) == (other.value + other.remaining)
    
    def __lt__(self,other):
        return (self.value + self.remaining) < (other.value + other.remaining)
    
    def __gt__(self,other):
        return (self.value + self.remaining) > (other.value + other.remaining)

class Heap:
    def __init__(self, initial_size = 10):
        self.cbt = [None for _ in range(initial_size)]        # initialize arrays
        self.next_index = 0                                   # denotes next index where new element should go

    def GetParent(self,index):
        parent = (index - 1) // 2
        return parent

    def GetChildren(self,index):
        right = (index + 1) * 2
        left = right - 1
        return left,right

    def SiftUp(self,index):
        parent = self.GetParent(index)
        if index == 0 or self.cbt[index] >= self.cbt[parent]:
            return
        else :
            temp = self.cbt[index]
            self.cbt[index] = self.cbt[parent]
            self.cbt[parent] = temp
            self.SiftUp(parent)

    def SiftDown(self,index):
        parent = index

        while parent < self.next_index:
            leftc, rightc = self.GetChildren(parent)
            parentval = self.cbt[parent]
            minval = parentval

            if leftc < self.next_index:
                leftcval = self.cbt[leftc]
                minval = min(leftcval,minval)

            if rightc < self.next_index:
                rightcval = self.cbt[rightc]
                minval =  min(rightcval,minval)

            if minval == parentval:
                return
            elif minval == leftcval:
                temp = self.cbt[parent]
                self.cbt[parent] = self.cbt[leftc]
                self.cbt[leftc] = temp
                parent = leftc
            else:
                temp = self.cbt[parent]
                self.cbt[parent] = self.cbt[rightc]
                self.cbt[rightc] = temp
                parent = rightc

    def is_empty(self):
        return self.next_index == 0

    def insert(self, data):
        if self.next_index >= len(self.cbt):
            self.ArrayFullHandler()
        self.cbt[self.next_index] = data
        self.SiftUp(self.next_index)
        self.next_index += 1

    def remove(self):
        if self.is_empty():
            return None
        else:
            self.next_index -= 1
            retval = self.cbt[0]
            self.cbt[0] = self.cbt[self.next_index]
            self.SiftDown(0)
            return retval

    def ArrayFullHandler(self):
        size = len(self.cbt) * 2
        new_cbt = [None for _ in range(size)]
        for i in range(len(self.cbt)):
            new_cbt[i] = self.cbt[i]
        self.cbt = new_cbt

def distance_between2p(point1,point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]

    c = math.sqrt((x * x) + (y * y))

    return c

def shortest_path(M,start,goal):
    explored = set()
    paths = Heap()
    
    paths.insert(Path([start],distance_between2p(M.intersections[start],M.intersections[goal])))

    while goal not in explored and not paths.is_empty():
        currPath = paths.remove()
        curr_Int = currPath.path[-1]

        for road in M.roads[curr_Int]:
            if road not in explored:
                new_value = currPath.value + distance_between2p(M.intersections[curr_Int],M.intersections[road])
                new_remaining = distance_between2p(M.intersections[road],M.intersections[goal])
                paths.insert(Path(currPath.path + [road],new_remaining,new_value))
                print(Path(currPath.path + [road],new_value))
        
        explored.add(curr_Int)
    
    return currPath.path