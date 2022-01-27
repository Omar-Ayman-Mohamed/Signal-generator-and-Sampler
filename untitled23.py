# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 07:02:51 2021

@author:Omar
"""

import os 
import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import *
from tkinter import ttk
from scipy import signal

visability = False
signal_number=0



def draw():
    siganl_to_be_sampled_fig.canvas.draw_idle()
    reconstructed_signal_fig.canvas.draw_idle()


#to create canvases and figuers


def fig_creation(name,graph_name,wheretoput):
    name,(graph_name)=plt.subplots(1)
    canvas = FigureCanvasTkAgg(name,
                                   master =wheretoput)        
        # placing the canvas on the Tkinter window
                   
    canvas.get_tk_widget().pack(fill = 'both',expand =True)
    return name,graph_name
    
    
signal_sumttion_list=[] #signal_sumttion_list is a static list containing the signals summation, static to avoid losing the summation after Composing,initiated as an empty list(no current sinusoidals)

signal_sumttion_list_index=[] #signal_sumttion_list_index is a static list supposed to carry the parameters of every sinusoidal in the list sino at same index

step=0.001

time= np.arange(0, 10,step) #creating a time interval during which signal will be visualized


def Composer(mag,freq,phase): #function that takes parameters of a sinusoidal and add it to the composed signal
    signal_sumttion_list.append(mag*np.sin(2*np.pi*time*freq+phase))#adding the new sinusoidal to the composed signal
    signal_sumttion_list_index.append([mag,freq,phase])
#signal_sumttion_list is a list containing signals, every signal is a list it self, which means signal_sumttion_list is a 2D list



def DeleteFromComposer(mag,freq,phase):# function that takes parameters of a previously added sinusoidal and removes it from the composed signal
    index=signal_sumttion_list_index.index([mag,freq,phase]) #retrieving the index of the sinusoidal required to be removed
    signal_sumttion_list.pop(index) #removing the desired sinusoidal from signal_sumttion_list based on it's index



def DeleteFromComposerByCB():#function to delet signals selected from combobox
    graph_for_signal_to_send.clear()
    index=added_signals.index(signals_cb.get())
    signal_sumttion_list.pop(index)
    if len(signal_sumttion_list) != 0:
        graph_for_signal_to_send.plot(time,sum(signal_sumttion_list))
    signal_to_send_fig.canvas.draw_idle()
    added_signals.pop(index)
    signals_cb['values'] = added_signals
    signals_cb.set('')
 


def Add():#function to add signals to each other 
    global final_time
    global final_amplitude
    global signal_number
    
    signal_number+=1
    graph_for_signal_to_send.clear()
    graph_for_added_signal.clear()
    mag=float(mag_var.get())
    freq=float(freq_var.get())
    phase=float(phase_var.get())
    magntiude_entry.delete(0, 'end')
    phase_entry.delete(0, 'end')
    freq_entry.delete(0, 'end')
    graph_for_added_signal.plot(time,mag*np.sin(2*np.pi*time*freq+phase))
    signal_to_be_added_fig.canvas.draw_idle()
    Composer(mag,freq,phase)
    added_signals.append('Phase: '+str(phase)+' Freq: '+str(freq))
    signals_cb['values'] = added_signals
    graph_for_signal_to_send.plot(time,sum(signal_sumttion_list))
    final_time = time
    final_amplitude = sum(signal_sumttion_list)
    signal_to_send_fig.canvas.draw_idle()


#def show():#to show signal before adding to composer
 #   graph_for_added_signal.clear()
  #  mag_temp=float(magntiude_entry.get())
   # freq_temp=float(freq_entry.get())
    #phase_temp=float(phase_entry.get())
    #graph_for_added_signal.plot(time,mag_temp*np.sin(2*np.pi*time*freq_temp+phase_temp))
    #signal_to_be_added_fig.canvas.draw_idle()



def send_to_main_graph():
    graph_for_signal_to_be_sampled.plot(final_time,final_amplitude)
    siganl_to_be_sampled_fig.canvas.draw_idle()

def sampling_button(self):
    Sampling_and_reconstruction(FmaxCalculate(final_amplitude),final_amplitude,time,sampling_slider.get(),graph_for_signal_to_be_sampled,graph_for_reconstructed_signal)
    draw()

        
def save_signal():
    saved_data = pd.DataFrame({"time_sec": final_time, "amplitude": final_amplitude})
    saved_data.to_csv("signal1.csv")


def openFile():
    global time
    global final_amplitude
    filepath = filedialog.askopenfilename(filetypes= (("csv files",".csv"),("all files",".*")))
    openFile.filepath = filepath
    file = open(filepath,'r')
    filename, extension = os.path.splitext(filepath)
    
    sampling_slider.set(0)

    if(extension == ".csv"):
     loaded_data = pd.read_csv( openFile.filepath)
     time = loaded_data["time_sec"] 
     final_amplitude = loaded_data["amplitude"]  
     frequencymax = FmaxCalculate(final_amplitude)
     Sampling_and_reconstruction(frequencymax,final_amplitude,time,0,graph_for_signal_to_be_sampled,graph_for_reconstructed_signal)
     draw()    
     print(filepath)
     file.close()
    else:
        openFile()
        


def FmaxCalculate(magnitude):#to calculate frequancy max
    fourierTransform = np.fft.fft(magnitude)/len(magnitude)# Normalize amplitude
    fourierTransform = fourierTransform[range(int(len(magnitude)/2))] # Exclude sampling frequency 
    magnitudes=abs(fourierTransform)
    pointsCount     = len(magnitude)

    values      = np.arange(int(pointsCount/2))

    timePeriod  = len(time)*step

    frequencies = values/timePeriod
    
    counter1=len(magnitudes)-1
    while magnitudes[counter1]<0.00000001:
        counter1-=1
    return (frequencies[counter1])
    
def Sample(signal,time,sampling_frequency):
    points_per_sec=(len(time)-1)/max(time)
    if (sampling_frequency==0):
        points_per_sample=len(signal)-1
    else:
        points_per_sample=int(points_per_sec/sampling_frequency)
    sample_index=0
    sampled_time=[]
    sampled_signal=[]
    while (sample_index < len(signal)):
        sampled_time.append(time[sample_index])
        sampled_signal.append(signal[sample_index])
        sample_index+=points_per_sample
    return sampled_time,sampled_signal

def Sampling_and_reconstruction(fmax,amplitude,time,sliderfactor,main_graph,reconstruction_graph):  
    main_graph.clear()
    reconstruction_graph.clear()
    sampling_freq.config(text=str(sampling_slider.get())+"fmax")
    sampling_freq_in_hz.config(text=str(int(sampling_slider.get()*fmax))+"hz")
    SamplingFrequancy = sliderfactor*(fmax)#nyqstfrequancy
    TimeDrawn,FrequancyDrawn = Sample(amplitude,time,SamplingFrequancy)#f
    
    main_graph.plot(time,amplitude)


        
   


    num_coeffs = len(TimeDrawn)  # sample points
    reconstruction = 0
    for reconstructionIndex in range(0, num_coeffs-1):  # since function is real, need both sides
        reconstruction += FrequancyDrawn[reconstructionIndex] * np.sinc(reconstructionIndex - SamplingFrequancy * time)


    main_graph_xmin,main_graph_xmax=main_graph.get_xlim()
    main_graph_ymin,main_graph_ymax=main_graph.get_ylim()
    reconstruction_graph.set_xlim([main_graph_xmin, main_graph_xmax])
    reconstruction_graph.set_ylim([main_graph_ymin, main_graph_ymax])
    reconstruction_graph.plot(time,reconstruction,color="green")
    if (sampling_slider.get() !=0):
        main_graph.scatter(TimeDrawn,FrequancyDrawn)
        main_graph.plot(time,reconstruction,linestyle='dashed')


           

        
        
    


root = tk.Tk()
#intializing varibles to use them in functions
signal_to_be_added_fig ='place holder'
signal_to_send_fig ='place holder 2'
graph_for_added_signal='place holder 3'
graph_for_signal_to_send= 'place holder 4'
siganl_to_be_sampled_fig = 'place holder 5'
graph_for_signal_to_be_sampled = 'place holder 6'

reconstructed_signal_fig = 'place holder 7'
graph_for_reconstructed_signal = 'place holder 8'
#signal generation input to take from user


mag_var=tk.StringVar(root)
phase_var=tk.StringVar(root)
freq_var=tk.StringVar(root)

#def getvalue():
    #print(mag_var.get())

#tab creation


tabControl = ttk.Notebook(root)  
signal_composer_tab = ttk.Frame(tabControl)
signal_viewer_tab = ttk.Frame(tabControl)
tabControl.add(signal_composer_tab, text ='Signal composer')
tabControl.add(signal_viewer_tab, text ='Signal viewer')
tabControl.pack(expand = True, fill ="both")


#frame for buttons andentery boxes

panel_frame = tk.Frame(signal_composer_tab)
panel_frame.pack(side = RIGHT,fill = 'y')

#frame for buttons andentery boxes
mid_panel =tk.Frame(panel_frame)
below_panel = tk.Frame(panel_frame)
added_signal_frame =tk.Frame(panel_frame)
added_signal_frame.pack(side =TOP)
mid_panel.pack(side = TOP,expand = True)
below_panel.pack(side=TOP,expand = True)
reconstructed_signal_frame = tk.Frame(signal_viewer_tab)
reconstructed_signal_frame.pack(side =BOTTOM,fill = 'both',expand =True)

def show_hide(): 
    global visability   
    if(visability == True):
          reconstructed_signal_frame.pack(fill ='both',expand =True)
          visability =False
         
    elif (visability == False): 
        reconstructed_signal_frame.pack_forget()
        visability = True
#combo box to  delete signals added


signal_to_be_deleted = tk.StringVar()
added_signals =[]
signals_cb = ttk.Combobox(below_panel, textvariable=signal_to_be_deleted)
signals_cb['values'] = added_signals
signals_cb['state'] = 'readonly'
delete_button = tk.Button(below_panel,text='Delete signal', command =DeleteFromComposerByCB,padx =35)
send_button = tk.Button(below_panel,text ='send',command = send_to_main_graph,padx =55)
save_button = tk.Button(below_panel,text ='save',command = save_signal,padx = 55)










#labels for enteries


magntiude_label = tk.Label(added_signal_frame, text = 'Magntiude')
phase_label = tk.Label(added_signal_frame, text = 'Phase')
freq_label = tk.Label(added_signal_frame, text = 'Frequency')


#entry creation and button creation


magntiude_entry = tk.Entry(added_signal_frame,textvariable = mag_var)
phase_entry = tk.Entry(added_signal_frame,textvariable = phase_var)
freq_entry = tk.Entry(added_signal_frame,textvariable = freq_var)
add = tk.Button(added_signal_frame,text='Add Signal',command=Add,padx =30)
#show = tk.Button(added_signal_frame,text='Confirm',command=show,padx = 35)



#entry and labels packing

    


magntiude_label.pack(side =TOP)
magntiude_entry.pack(side=TOP)
phase_label.pack(side =TOP)
phase_entry.pack(side=TOP)
freq_label.pack(side=TOP)
freq_entry.pack(side=TOP)
#show.pack(side=TOP)
add.pack(side=TOP)
signals_cb.pack(side=TOP)
delete_button.pack(side=TOP)
send_button.pack(side=TOP)
save_button.pack(side=TOP)


signal_to_be_added_fig, graph_for_added_signal=fig_creation(signal_to_be_added_fig, graph_for_added_signal,signal_composer_tab)
signal_to_send_fig, graph_for_signal_to_send=fig_creation(signal_to_send_fig, graph_for_signal_to_send,signal_composer_tab)

buttons_frame = tk.Frame(signal_viewer_tab)
buttons_frame.pack(side =TOP,fill = 'both')
to_be_sampled_signal_frame = tk.Frame(signal_viewer_tab)

sampling_slider = Scale(to_be_sampled_signal_frame,from_=0,to =3,orient =HORIZONTAL,command=sampling_button,resolution=0.05,length=500,showvalue=0)
open_signal = tk.Button(buttons_frame,text ='open signal',command = openFile)
show_reconstructed = ttk.Button(buttons_frame,text ='Toggle visability',command = show_hide)
open_signal.pack(side = LEFT)
#open_signal.place(x= 0,y=0)
show_reconstructed.pack(side = LEFT)
#show_reconstructed.place(x=72,y=0)
sampling_slider.set(0)
sampling_freq = tk.Label(to_be_sampled_signal_frame, text="0.0fmax")
sampling_freq_in_hz = tk.Label(to_be_sampled_signal_frame, text="0.0hz")
to_be_sampled_signal_frame.pack(side =TOP,fill = 'both',expand =True)





siganl_to_be_sampled_fig,graph_for_signal_to_be_sampled=fig_creation(siganl_to_be_sampled_fig, graph_for_signal_to_be_sampled, to_be_sampled_signal_frame)
sampling_freq_in_hz.pack(side = BOTTOM)
sampling_freq.pack(side = BOTTOM)
sampling_slider.pack(side = BOTTOM)




reconstructed_signal_fig,graph_for_reconstructed_signal = fig_creation(reconstructed_signal_fig, graph_for_reconstructed_signal, reconstructed_signal_frame)

 
root.mainloop()