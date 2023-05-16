from pymongo import MongoClient as Mng
import pandas as pd

def DATABASE():

    connect = Mng(host='localhost',port = 27017)
    python = connect.python
    Premier_League = python.Premier_League

    global Data

    Data=[]
    for i in Premier_League.find():
        Data.append(i)
    

DATABASE()


Chart = pd.DataFrame(Data,index=(range(1,31)))

Chart.drop(['_id'] ,axis=1 ,inplace=True)
Chart.rename(columns={'Salary':'Salary(Euro)','Player':'Players','Team':'Teams'} ,inplace=True)

Chart.sort_values('Salary(Euro)',ascending=False ,inplace=True)

#_______________________________________________________________________________  # Top 10 
Top_10_Slr = []
Top_10_Ply = []

for i in Chart.index:
    if i <= 10:
        Top_10_Ply.append((Chart['Players'].loc[i]))
        Top_10_Slr.append(Chart['Salary(Euro)'].loc[i])

with open('Top_10.txt','w') as File:
    File.write(f'{Top_10_Ply}')
    File.write('\n')
    File.write(f'{Top_10_Slr}')
    
#_______________________________________________________________________________ # Teams Payments

print('\n',20 *' ','The Teams Payments Weekly (Euro)\n')

def Teams_Payments():

    Clubs = {}
    for i in Chart.index:
        Clubs[Chart['Teams'].loc[i]] = Clubs.get(Chart['Teams'].loc[i] , 0 ) + Chart['Salary(Euro)'].loc[i]

    Sort_Clubs ,Salary_Edit = [],[]
    Counter = 0
    Salaries ,W = '',''

    for k,v in sorted(Clubs.items()):
        Sort_Clubs.append(k)
        Salaries += str(v) 

        for i in Salaries.split(): 
            for w in i[::-1]:
                Counter +=1
                W +=w

                if (len(i) > Counter) and (Counter == 3):
                    W +=','

                elif (len(i) > Counter) and (Counter == 6):
                    W +=','

            Counter = 0
            Salary_Edit.append(W[::-1])
            Salaries,W = '',''


    Total_CLubs_Salary = {}
    for k,v in zip(Sort_Clubs,Salary_Edit):
        Total_CLubs_Salary[k]=v

    List_Edit= []
    for i,x in Clubs.items():
        List_Edit.append((x,i))

    List_Edit.sort(reverse=True)

    for i in List_Edit:

        if i[1] in Total_CLubs_Salary.keys():
            print(f'{i[1]:16} : {Total_CLubs_Salary[i[1]]:10}Euro')

        with open('Premier_League.txt','a',newline='') as Write:    
                Write.write(i[1])
                Write.write('   ')
                Write.write(Total_CLubs_Salary[i[1]])
                Write.write('\n')

                
Teams_Payments()
