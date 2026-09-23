'''
Quantum Phase Estimation

By Abdulah Amer


T gate leaves |0> state alone and adds a phase of e^pi/4 to
|1> state. Quantum Phase Estimation measures theta where
T|1> = e^2ipitheta|1>

First n-1 qubits are used for the protocol and get measured

the nth qubit is put into the eigenstate of the operator whose phase
we are measuring this is important

'''


from qiskit import *
import numpy as np

from math import *
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


from fractions import Fraction


S_simulator=Aer.backends(name='statevector_simulator')[0]
M_simulator=Aer.backends(name='qasm_simulator')[0]


# # a circuit with 4 qubits and 3 classical bits
#
# n=4 #number of qubits
# m=3 #number of classical bits
#
# # a circuit with n qubits and m classical
# qc=QuantumCircuit(n,m)
#
# qc.x(3)
#
# for qubit in range(3):
#     qc.h(qubit)
#
# #Now estimate phase for T gate with phase of pi/4
# # apply the T gate a bunch of times
#
# reps=1
# for counting_qubit in range(3):
#     for i in range(reps):
#         #applies T gate using the counting qubits as control
#         #qubits and the last qubit as the target qubit.
#         #
#         qc.cu1(pi/4, counting_qubit, 3)
#
#     reps *=2 #doubles the number of T gates to each adjacent qubit
#
#
# qc.draw(output='mpl')
#
#
# #Do the inverse qft to find the state
#
def qft_inverse(qc,n):

    for qubit in range(n//2): #floor division for odd number of qubits
        qc.swap(qubit, n-qubit-1)

        #swaps the current qubit with n-qubit-1

    for j in range(n):
        for m in range(j):
            qc.cu1(-pi/float(2**(j-m)),m,j)
        qc.h(j)

#
#
# qc.barrier()
#
# qft_inverse(qc,3)
#
# qc.barrier()
#
# for n in range(3):
#     qc.measure(n,n)
#
#
# #qc.draw(output='mpl')
#


#lol
#
#
# results=execute(qc,backend=M_simulator, shots=4096).result()
# histogram=results.get_counts()
#
# plot_histogram(histogram)

# After measurement we divide the decimal equivalent by 2^n
# 1/2^3 =1/8 , theta =1/8, therefore e^2ipitheta = e^ipi/4
#Which is the phase added by the T gate.


#This was a pretty trivial result since we perfectly get
#one highest probability


#make functions to generalize even better


# def prepQPE(qc, n,m): #prepares the circuit
#     for qubit in range(m):
#         qc.h(qubit)
#
#     qc.x(m)
#
#
# def CU(theta, qc, n,m): #performs controlled unitary operations
#
#     prepQPE(qc,n,m)
#
#     angle=theta
#     reps=1
#     for counting_qubit in range(m):
#         for i in range(reps):
#             qc.cu1(angle, counting_qubit,5)
#         reps*=2
#

#Let us also Automate more of the process so we can scale these things
#To learn even more from them


'''
Note we are making circuits to measure known thetas
But we will try to build up to design a circuit to do
Arbitrary Phase Estimation

'''
#Makes an isntance of a quantum circuit that runs the QPE protocol
def makeQPE(theta, n): #m=n-1
    m=n-1
    qc=QuantumCircuit(n,m)
    #Prep
    for qubit in range(m):
        qc.h(qubit)

    qc.x(m)
    #CU1 gates
    reps=1
    for counting_qubit in range(m):
        for i in range(reps):
            qc.cu1(theta, counting_qubit, m)
        reps*=2
    qc.barrier()

    qft_inverse(qc,m)

    qc.barrier()

    for n in range(m):
        qc.measure(n,n)

    return qc

#gets out results and aquires the one with the most hits
def get_results(q,n):

    m=n-1

    results=execute(q, backend=M_simulator).result()
    histo=results.get_counts()

    higher=0
    hits=histo.values()
    for i in hits:
        if i>higher:
            higher=i

    newhisto=dict([(value,key) for key, value in histo.items()])

    answer=int(newhisto[higher],2)

    check=(answer/(2**m))
    return check

#simple finding error function
def error(expected, actual):
    expected_minus_actual=abs(expected-actual)
    percent_error=expected_minus_actual/100

    return percent_error

#tie it all together
def graph_qubits_error(piece_of_pi, qubits):
    #set up
    angle=pi*piece_of_pi
    expected=(piece_of_pi/2)
    qubits=[]
    results=[]
    errors=[]

    n=2
    while n<=qubits:
        #make circuit and measure
        q=makeQPE(angle,n)
        actual=get_results(q,n)
        #our error
        err=error(expected, actual)
        #Dont forget how to graph
        qubits.append(n)
        results.append(actual)
        errors.append(err)
        n+=1
    #Plotting##########
    # plt.figure(1)
    # plt.title('Value vs qubits used')
    # plt.plot(qubits,results, color='green', label='Experimental Result')
    # plt.hlines(expected,2,16, color='blue', linestyles='dashed', label=' Expected Value')
    # plt.xlabel('Number of Qubits')
    # plt.ylabel('Result of Measurement')
    #
    #
    # plt.figure(2)
    # plt.title('Error vs qubits used')
    # plt.plot(qubits, errors)
    # plt.xlabel('Number of Qubits')
    # plt.ylabel('Percent Error')
    # plt.show()


piece_of_pi=1/2
qubits=8
#graph_qubits_error(piece_of_pi,qubits)

def error_per_slice(piece_of_pi, qubits):
        angle=pi*piece_of_pi
        expected=(piece_of_pi/2)
        q=makeQPE(angle,qubits)
        actual=get_results(q,qubits)
        err=error(expected, actual)

        return err


def  yeet():
    slices=[]
    list_of_errors=[]
    qubits=5
    i=1
    while i<=16:
        piece_of_pi=1/i
        slices.append(piece_of_pi)
        list_of_errors.append(error_per_slice(piece_of_pi, qubits))
        i+=1
    title= ('Error for different slices of pi using '+ str(qubits)+ ' qubits')
    plt.title(title)
    plt.plot(slices,list_of_errors, color='green')
    #plt.hlines(expected,2,16, color='blue', linestyles='dashed', label=' Expected Value')
    plt.xlabel('Slices')
    plt.ylabel('Error in measurement')

    #plt.show()

    return list_of_errors

def get_slices():
    slices=[]
    i=1
    while i<=16:
        piece_of_pi=1/i
        slices.append(piece_of_pi)
        i+=1
    return slices

'''
some stuff to look at the fractions
'''
def frac_stuff(slices):
    integers=[]
    for i in range(len(slices)):

        two_to_the_n=2**(qubits-1)
        it_theta=slices[i]
        integers.append(two_to_the_n*it_theta)

    fracslices=[]
    for i in range(len(slices)+1):
        piece='1/' + str(i)
        fracslices.append(piece)

    #gets rid of the 1/0 at the front of the list
    fracslices.pop(0)
    #inserts a 1 instead of 1/1 in our list
    fracslices.insert(0,1)
    #gets ride of 1/1
    fracslices.pop(1)
    '''
    Make a Table!
    '''
    Dabois=yeet()
    header=['2^n*', 'Slice']
    head1='2^n*'+ 'Theta'
    head2='Slice'
    head3='Error amounts'
    col1=integers
    col2=fracslices
    col3=Dabois
    from tabulate import tabulate


    table=tabulate({head2: col2, head1: col1, head3:col3}, headers='keys', tablefmt='github')
    for i in range(len(col1)):
        print(col2[i], '&' , round(col1[i],5), '&', round(col3[i],5))
    return table

#print(table)

from qiskit.visualization import plot_bloch_vector
'''

The following code is execute in Jupyter notebooks file called QPE final
It gives us images Rx and Ry respectively

#Rx
q=QuantumRegister(1, 'l')
blocher=QuantumCircuit(q)
blocher.ry(pi/2,0)
bloch_job=execute(blocher, S_simulator).result()
plot_bloch_multivector(bloch_job.get_statevector(blocher), title='initial')

#Ry
blocher=QuantumCircuit(q)
blocher.ry(pi/2,0)
blocher.u1(pi/2,0)
bloch_job=execute(blocher, S_simulator).result()
plot_bloch_multivector(bloch_job.get_statevector(blocher), title='final')
'''

piece_of_pi=1/4
qubits=3


q=makeQPE(piece_of_pi,qubits)
#q.draw(output='mpl').savefig('The Circuit is Here.png')

print(frac_stuff(get_slices()))
