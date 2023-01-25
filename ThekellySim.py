import numpy
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

def trial(p):
    #print('p = ', p)
    #print('random = ', numpy.random.random())
    if numpy.random.random() < p:
        return 1
    else:
        return 0
    
    
    
def bets( wager, p = 0.5, Total_money = 1000, loss_f = 1, profit_f = 1):
    if trial(p):
        change = wager * profit_f * Total_money * 0.01
    else:
        change = wager * -(loss_f) * Total_money * 0.01
    Total_money += change
    return Total_money

def gmean(a):
    a = np.log(a)
    a = np.mean(a,axis = 0)
    a = np.exp(a)
    return a

def bet(wager1, wager2, p, money_class, money_kelly, a, b):
    
    sim_n = 3 * st.session_state.m
    step = 2 * st.session_state.m
    np1 = np.zeros((sim_n,step))
    wager1 = st.session_state.wager1
    for i in range(sim_n):
        for j in range(step):
            if j == 0:
                if st.session_state.count == 0:
                    np1[i,j] = money_class[-1]
                    continue
                np1[i,j] = bets(wager1, p, st.session_state.sim_trials_1[-1,i], a, b)
                continue
            np1[i,j] = bets(wager1, p, np1[i,j-1], a, b)
    if st.session_state.count == 0:
        st.session_state.sim_trials_1 = np1.T
    else: 
        st.session_state.sim_trials_1 = np.append(st.session_state.sim_trials_1, np1.T, axis = 0)
    money_class = np.append(money_class, gmean(np1))
    # print(money_class)
    
    np2 = np.zeros((sim_n,step))
    for i in range(sim_n):
        for j in range(step):
            if j == 0:
                if st.session_state.count == 0:
                    np2[i,j] = money_kelly[-1]
                    continue
                np2[i,j] = bets(wager2, p, st.session_state.sim_trials_2[-1,i], a, b)
                continue
            np2[i,j] = bets(wager2, p, np2[i,j-1], a, b)
    
    if st.session_state.count == 0:
        st.session_state.sim_trials_2 = np2.T
    else:
        st.session_state.sim_trials_2 = np.append(st.session_state.sim_trials_2, np2.T, axis = 0)
        
    
    money_kelly = np.append(money_kelly, gmean(np2))

    #print('money_class::',st.session_state.sim_trials_1)
    #print('money_kelly::',st.session_state.sim_trials_2)
    st.session_state.money_class = money_class
    st.session_state.money_kelly = money_kelly
    st.session_state.count += 1
def reset():
    st.session_state.money_class = np.array([100])
    st.session_state.money_kelly = np.array([100])
    st.session_state.count = 0
    st.session_state.sim_trials_1 = np.array([0])
    st.session_state.sim_trials_2 = np.array([0])

    return



st.header("Kelly vs Gambler Simulation")
st.write('---')
st.subheader('The Formula')
st.latex(r'''
         
         
         f(\%age) = \frac{p*k - q*a}{a*k}
         
         
         ''')
st.write('---')


p = st.slider('Probability of winning(P):', 0.0, 1.0, 0.5)
num_player = st.slider('Profit Multiplier(K):', 0.0, 3.0, 1.0)
a = st.slider('Loss Multiplier(A):', 0.0, 3.0, 1.0)
total = st.number_input('Total amount of money:', 1, 1000, 100)  


st.write('---')


q = 1-p
q = round(q, 2)
#a = 1
b = num_player

if 'money_class' not in st.session_state:
    st.session_state.money_class = np.array([total])
if 'money_kelly' not in st.session_state:
    st.session_state.money_kelly = np.array([total])
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'wager1' not in st.session_state:
    st.session_state.wager1 = 5
if 'sim_trials_1' not in st.session_state:
    st.session_state.sim_trials_1 = np.array([0])
if 'sim_trials_2' not in st.session_state:
    st.session_state.sim_trials_2 = np.array([0])
if 'm' not in st.session_state:
    st.session_state.m = 1
    
    
    
st.session_state.money_class[0] = np.array([total])
st.session_state.money_kelly[0] = np.array([total])




st.write('Probability of winning (P):', p)
st.write('Probability of losing (Q):', q)
st.write('Odds against ratio (K : A):', b, ' : ',a)
st.write('Starting money:', total)

#p = st.button('randomize profit', on_click=randp)
st.write('---')

with st.container():
    
    row1, row2 = st.columns(2)


    with row1:
        st.subheader('*Gambler*')
        st.write('Wager:', st.session_state.wager1)
        st.write('Money in Hand:',st.session_state.money_class[-1])
        
        

    with row2:
        st.subheader('*Kelly*')
        wager2 = (p*b - q*a) / (a*b)
        wager2 = wager2 * 100
        if wager2 < 0:
            wager2 = 0
        st.write('Wager:', wager2)
        st.write('Money in Hand:',st.session_state.money_kelly[-1])
    
        

    betr1, betr2 = st.columns(2)
    st.write('---')
    betr3, betr4 = st.columns(2)
    
    with betr4:
        meow = st.button('Bet', on_click=bet, args=(st.session_state.wager1, wager2, p, st.session_state.money_class, st.session_state.money_kelly,a,b))
    with betr1:
        st.session_state.wager1 = st.number_input('Wager for gambler:', 1, 100, 5,1)  
    with betr3:
        resetbutton = st.button('Reset', on_click=reset)
    with betr2:
        #put a drop down to select m
        if st.session_state.count < 1:
            st.session_state.m = st.selectbox('Select simulator multiplier:', [1,10,100])
        else:
            #disable the drop down
            st.session_state.m = st.selectbox('Select simulator multiplier:', [1,10,100],disabled=True)
    st.write('---')
    if st.session_state.count > 0:
        st.write('Number of bets:', (st.session_state.count * st.session_state.m * 2)-1,"    |     Number of simulations:", st.session_state.m * 3)
    else:
        st.write('Number of bets:', 0, "    |     Number of simulations:", st.session_state.m * 3)
    
    #open a toggle menu
    with st.expander('Show simulation trials'):
        ebetr1, ebetr2 = st.columns(2)
        with ebetr1:
            st.write('Gambler:')
            st.line_chart(st.session_state.sim_trials_1)
        with ebetr2:
            st.write('Kelly:')
            st.line_chart(st.session_state.sim_trials_2)

#print('money_class', st.session_state.money_class)
#print('money_kelly', st.session_state.money_kelly)
    st.write(" ")
    st.write('---')
    st.write(' ')
    tota_moneyy = np.array([st.session_state.money_class, st.session_state.money_kelly]).T
    tota_moneyy = pd.DataFrame(tota_moneyy, columns = ['Gambler', 'Kelly'])
    st.line_chart(tota_moneyy)


