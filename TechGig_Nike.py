''' Read input from STDIN. Print your output to STDOUT '''
    #Use input() to read input from STDIN and use print to write your output to STDOUT

def optimalShopping(itemCost,Amt):
    Total=0
    Count=0
    AmtExhaust=0
    AmtCostList=[]
    itemCost.sort()

    for i,v in enumerate(itemCost):
        if (Amt - (Total + v))>=0:
            Total+=v
            Count+=1
        else:
            AmtExhaust=1
    
    if AmtExhaust==1:
        RemainingAmt=-1
    else:
        RemainingAmt=Amt-Total
    
    AmtCostList.append(RemainingAmt)
    AmtCostList.append(Count)
    return AmtCostList

def main():
    firstLine=input().split(' ')
    N=int(firstLine[0])
    D=int(firstLine[1])
    itemCost=[int(i) for i in input().split(" ")]

    RemainingAmt=D
    NetCount=0
    while (RemainingAmt>0):
        AmtCostList=optimalShopping(itemCost,RemainingAmt)
        RemainingAmt=AmtCostList[0]
        TempCount=AmtCostList[1]
        NetCount+=TempCount
    print(NetCount)

main()

