from flask import Flask, render_template
import time
import threading
import datetime
import math
app = Flask(__name__) 

class Node:
    def __init__(self, data, TSaddr, targetTAS, flg, period, reservPerson):
        self.data = int(data) #time value
        self.TSaddress = str(TSaddr)
        self.TASToMove = str(targetTAS)
        self.StartingFlg = bool(flg)
        self.ReservePeriod = int(period)
        self.reservingPerson = str(reservPerson)
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def asc_ordered_list(self, data, TSaddr, userAccount, flg, period, reservPerson):
        #high -> low
        new_node = Node(data,TSaddr, userAccount, flg, period, reservPerson)
        if self.head is None:
            self.head = new_node
            return

        temp = self.head
        if temp.data > data:
            new_node.next = temp
            self.head = new_node
            return


        while temp.next:
            if temp.next.data >= data:
                if (str(TSaddr) == temp.next.TSaddress) and (temp.StartingFlg == True and temp.next.StartingFlg == False):
                    temp = temp.next
                break
            temp = temp.next

        new_node.next = temp.next
        temp.next = new_node

    def desc_ordered_list(self, data,TSaddr, userAccount, flg, period,reservPerson):
        #low -> high
        new_node = Node(data, TSaddr, userAccount, flg, period,reservPerson)
        if self.head is None:
            self.head = new_node
            return

        temp = self.head
        if data > temp.data:
            new_node.next = temp
            self.head = new_node
            return

        while temp.next:
             if temp.data > data and temp.next.data < data:
                 break
             temp = temp.next

        new_node.next = temp.next
        temp.next = new_node

    def remove_head(self):
        if self.head is None:
            return

        temp = self.head
        self.head = self.head.next

        del temp

    def calculate_time_value(self, timeVal):
        return (timeVal - time.time()) / 5

    def reserve(self, data, TSaddr, relocateAddr, returningAddr, period, reservPerson):
        # tempReturnAddr = self.getReturnTASAddress(TSaddr)
        # if (tempReturnAddr is not None) and (returningAddr != tempReturnAddr):
        #     returningAddr = tempReturnAddr

        if self.head == None:
            #if empty, reserve
            self.asc_ordered_list(data,TSaddr, relocateAddr, True, period, reservPerson)
            self.asc_ordered_list(data + period,TSaddr, returningAddr, False, period, reservPerson)
            return

        if data < self.head.data:
            if data + period <= self.head.data:
                print("reserve to head")
                self.asc_ordered_list(data,TSaddr, relocateAddr, True, period, reservPerson)
                self.asc_ordered_list(data + period,TSaddr, returningAddr, False, period, reservPerson)
                return
            else:
                if str(TSaddr) == self.head.TSaddress:
                    print("interfere from the front")
                    return

        Start_temp = self.head
        #print("head val = ", Start_temp.data)
        prevNode = Start_temp
        nextNode = Start_temp.next

        #starting node
        while Start_temp.next:
            #move until the sorted place
            if Start_temp.data > data:
                print("break")
                break
            #print("prev val = ", prevNode.data)
            #print("watching val = ", Start_temp.data, ", comp val = ", data)
            if str(TSaddr) == Start_temp.TSaddress:
                prevNode = Start_temp
            Start_temp = Start_temp.next
            if Start_temp.next != None:
                nextNode = Start_temp.next
            else:
                if(data >= Start_temp.data):
                    print("reserve to tail")
                    self.asc_ordered_list(data,TSaddr, relocateAddr, True, period, reservPerson)
                    self.asc_ordered_list(data + period,TSaddr, returningAddr, False, period, reservPerson)
                    return

        #print("=====================")
        #print("prev val = ", prevNode.data)
        #print("watching val = ", Start_temp.data)
        #print("next val = ", nextNode.data)
        #print("=====================")

        if (prevNode.StartingFlg == True) and (prevNode.TSaddress == str(TSaddr)):
            #if the prev node's flag is Starting, which means current reservation
            #interfere other reservation
            print("Cannot reserve : interfere from start1, startval = ", prevNode.data, " ", prevNode.StartingFlg)
            return
        else:
            if (Start_temp.StartingFlg == False) and (Start_temp.TSaddress == str(TSaddr)):
                #if the next node's flag is finishing, which means current reservation
                #interfere other reservation
                print("Cannot reserve : interfere from end1, startval = ", nextNode.data, " ", Start_temp.StartingFlg)
                return
            else:
                #prev node's flag is finishing and next node's flag is starting
                #means current reservation is between two reserved slots.
                # == reservable
                print("Reservable Starting Node1")

        Finish_temp = self.head
        prevNode = Finish_temp
        nextNode = Finish_temp.next
        #starting node
        while Finish_temp.next:
            #move until the sorted place
            if Finish_temp.data >= data+period:
                print("break")
                break
            if str(TSaddr) == Finish_temp.TSaddress:
                prevNode = Finish_temp
            Finish_temp = Finish_temp.next
            if Finish_temp.next != None:
                nextNode = Finish_temp.next
        

        #print("=====================")
        #print("prev val 1= ", prevNode.data)
        #print("prev val flg 1= ", prevNode.StartingFlg)
        #print("watching val 1= ", Finish_temp.data)
        #print("next val 1= ", nextNode.data)
        #print("=====================")
        if (prevNode.StartingFlg == True) and (prevNode.TSaddress == str(TSaddr)):
            #if the prev node's flag is Starting, which means current reservation
            #interfere other reservation
            print("Cannot reserve : interfere from start2")
            return
        else:
            if (Finish_temp.StartingFlg == False) and (Finish_temp.TSaddress == str(TSaddr)):
                #if the next node's flag is finishing, which means current reservation
                #interfere other reservation
                print("Cannot reserve : interfere from end2")
                return
            else:
                #prev node's flag is finishing and next node's flag is starting
                #means current reservation is between two reserved slots.
                # == reservable
                print("Reservable Finishing Node2")


        #print("s = ", Start_temp.data, "c = ", Start_temp.next.data, "f =", Finish_temp.data)
        if (Start_temp != Finish_temp) and (Start_temp.TSaddress == str(TSaddr)) and (Finish_temp.TSaddress == str(TSaddr)):
            print("Current reservation covers other reservation")
            return
        else:
            #reserve function
            print("Do reserve")
            self.asc_ordered_list(data,TSaddr, relocateAddr, True, period, reservPerson)
            self.asc_ordered_list(data + period,TSaddr, returningAddr, False, period, reservPerson)

    def display_list(self):
        relocatingTsList = []
        temp = self.head
        print("current list")
        while temp is not None:
            temp.data -= 1
            if(temp.data == 0):
                relocatingTsList.append((temp.TSaddress, temp.TASToMove, temp.StartingFlg))
                temp = temp.next
                self.remove_head()
            else:
                print("data = {0} {1} {2} {3} {4}".format(temp.data, temp.TSaddress, temp.TASToMove, temp.StartingFlg, temp.ReservePeriod))
                temp = temp.next

        #threading.Timer(30, self.display_list).start()
        return relocatingTsList

    def showList(self):
        temp = self.head
        while temp is not None:
            print("data = {0} {1} {2} {3} {4}".format(temp.data, temp.TSaddress, temp.TASToMove, temp.StartingFlg, temp.ReservePeriod))
            temp = temp.next

    def checkPeriod(self, mon1, dat1, hou1, min1, ampm1, mon2, dat2, hou2, min2, ampm2):
        startTimeval = self.checkTime(mon1, dat1, hou1, min1, ampm1)
        endTimeval = self.checkTime(mon2, dat2, hou2, min2, ampm2)

        result = endTimeval - startTimeval
        if result > 0:
            return int(startTimeval), int(endTimeval - startTimeval)
        else:
            return int(-1), int(-1) #denied

    def checkTime(self, month, date, hour, minute, ampm):
        reservingYear = datetime.datetime.now().year

        if(ampm == 1):
            hour += 12
        reservingTime = datetime.datetime(int(reservingYear), month, date, hour, minute)
        now = datetime.datetime.now()
    
        print(now)
        print(reservingTime)
        print((reservingTime - now).days)
        if (reservingTime - now).days < 0: #the past
            reservingYear += 1 #make it future
            reservingTime = datetime.datetime(reservingYear, month, date, hour, minute)

        howFarFromNow = (reservingTime - now).seconds + ((reservingTime - now).days * 24*60*60)
        howFarFromNow = math.ceil(howFarFromNow/300) + 1
        print(howFarFromNow)

        return int(howFarFromNow)

    def countTsReservationList(self, tsaddrToSearch):
        countedReservedTsList = []
        if self.head is None:
            return countedReservedTsList
            
        temp = self.head
        tas2move = ""
        while temp is not None:
            if(temp.TSaddress == str(tsaddrToSearch)) and (temp.StartingFlg == True):
                tas2move = temp.TASToMove
            elif(temp.TSaddress == str(tsaddrToSearch)) and (temp.StartingFlg == False):
                #Since the node delete from the start.
                startRealTime = getRealTimeFromTimeval(temp.data - temp.ReservePeriod)
                endRealTime = getRealTimeFromTimeval(temp.data)
                if temp.data - temp.ReservePeriod <= 0:
                    isMiddleOfReservedPeriod = True
                else:
                    isMiddleOfReservedPeriod = False
                countedReservedTsList.append((temp.reservingPerson, tas2move, startRealTime, endRealTime, isMiddleOfReservedPeriod))
            temp = temp.next
        
        return countedReservedTsList

    def getReturnTASAddress(self, tsaddrToSearch):
        tempAddr = None
        if self.head is None:
            return None

        temp = self.head
        while temp is not None:
            if(temp.TSaddress == str(tsaddrToSearch)) and (temp.StartingFlg == False):
                tempAddr = temp.TASToMove
                break
        
        return tempAddr

    def cancelReserve(self, tsaddrToCancel, index):
        print (self.head)
        if self.head is None:
            return

        counter = index
        tempStartNode = None
        tempEndNode = None
        temp = self.head
        if(temp.TSaddress == str(tsaddrToCancel)) and (temp.StartingFlg == True):
            tempStartNode = temp

        while (temp.next is not None) and (counter > 0):
            print(temp.next.TSaddress, temp.next.StartingFlg)
            if(temp.next.TSaddress == str(tsaddrToCancel)) and (temp.next.StartingFlg == True):
                tempStartNode = temp
            elif (temp.next.TSaddress == str(tsaddrToCancel)) and (temp.next.StartingFlg == False):
                tempEndNode = temp
                counter = counter - 1
            temp = temp.next
            print("index", counter)

        if counter > 0:
            return

        #print("tempStartNode", tempStartNode.next.TSaddress)
        #print("tempEndNode", tempEndNode.next.TSaddress)

        if tempEndNode is not None:
            tempPtr = tempEndNode.next
            tempEndNode.next =  tempEndNode.next.next
            del tempPtr

        if tempStartNode is not None:
            if tempStartNode == self.head:
                self.remove_head()
            else:
                tempPtr = tempStartNode.next
                tempStartNode.next =  tempStartNode.next.next
                del tempPtr       

        return

def getRealTimeFromTimeval(timeval_):
    currentTime = datetime.datetime.now()
    print(currentTime.minute)
    #howFarFromNowToMin should care uncounted minutes (less than 5 min)
    howFarFromNowToMin = (timeval_ * 5) - ((currentTime.minute)%5)
    realTime = currentTime + datetime.timedelta(minutes=howFarFromNowToMin)
    realTime = realTime.strftime('%Y-%m-%d %H:%M')
    return realTime


#print( getRealTimeFromTimeval(5))
# llist = LinkedList()
# llist.reserve(23,4,56,23,3,12)
# print(llist.display_list())

# llist.cancelReserve(4,1)
# print(llist.display_list())