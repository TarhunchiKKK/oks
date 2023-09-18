from tkinter import *
from tkinter import ttk


port_number = 1
bits_number = 8


port_numbers = ["COM1", "COM2", "COM3", "COM4"]
bit_numbers = ["5", "6", "7", "8"]



first_row_height = 0.7
second_row_height = 0.3

first_column_width = 0.495
second_column_width = 0.495


def bits_number_selected(event):
    global bit_numbers
    #bit_numbers = 



# for global values



root = Tk()
root.title("Serial Port")
root.geometry("650x750")
#root.resizable(False, False)              # can't resize block

root.minsize(500, 600)


# окно ввода
input_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10], width=320, height=500);
input_frame.place(relwidth=first_column_width, relheight=first_row_height, relx=0.0, rely=0.0)
input_frame_header = ttk.Label(input_frame, text="Input Window", font=("Arial", 16))
input_frame_header.pack()


# окно вывода
output_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10], width=320, height=500);
output_frame.place(relwidth=second_column_width,relheight=first_row_height, relx=0.01 + second_column_width, rely=0.0)
output_frame_header = ttk.Label(output_frame, text="Output Window", font=("Arial", 16))
output_frame_header.pack()


# окно контроля
control_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10], width=320, height=200);
control_frame.place(relwidth=first_column_width, relheight=second_row_height, relx=0.0, rely=0.71)

control_frame_header = ttk.Label(control_frame, text="Control Window", font=("Arial", 16))
control_frame_header.grid(row=0, column=0, columnspan=2)




port_label = ttk.Label(control_frame, text="Port number:", font=("Arial", 16))
port_label.grid(row=1, column=0)
port_number_combobox = ttk.Combobox(control_frame, values=port_numbers, state="readonly")
port_number_combobox.grid(row=1, column=1)



bits_number_label = ttk.Label(control_frame, text="Bits number:", font=("Arial", 16))
bits_number_label.grid(row=2, column=0)
bits_number_combobox = ttk.Combobox(control_frame, values=bit_numbers, state="readonly")
bits_number_combobox.grid(row=2, column=1)




# окно статуса
status_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10], width=320, height=200);
status_frame.place(relwidth=second_column_width, relheight=second_row_height, relx=0.01 + second_column_width, rely=0.71)
status_frame_header = ttk.Label(status_frame, text="Status Window", font=("Arial", 16))
status_frame_header.pack()


root.mainloop()