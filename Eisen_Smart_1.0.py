import tkinter as tk


class EntryData:
    def __init__(self, spcfc, meass, rewrd, impor, urgcy):
        self.spcfc = spcfc
        self.meass = meass
        self.rewrd = rewrd
        self.impor = impor
        self.urgcy = urgcy
        self.taskinfo = ''
        self.quadrant = ''

        if self.spcfc != '':
            self.taskinfo += 'I want to ' + self.spcfc
            if self.meass != '':
                self.taskinfo += ' by ' + self.meass
            if self.rewrd != '':
                self.taskinfo += ' to get ' + self.rewrd

        thrshld = 5
        if self.urgcy >= thrshld and self.impor >= thrshld:
            self.quadrant = 'hihi'
        elif self.urgcy >= thrshld > self.impor:
            self.quadrant = 'hilo'
        elif self.urgcy < thrshld <= self.impor:
            self.quadrant = 'lohi'
        else:
            self.quadrant = 'lolo'


ED_OBJ_LST = []


def save_to_global_lst(entry_data_obj):
    ED_OBJ_LST.append(entry_data_obj)


def create_screen(master, mode, obj_to_remove=0, quadrant_to_draw=''):
    # icons originate from: https://www.kenney.nl/assets/game-icons
    back_btn_img = tk.PhotoImage(file='icons/arrowLeft.png')
    confirm_btn_img = tk.PhotoImage(file='icons/checkmark.png')
    addtask_btn_img = tk.PhotoImage(file='icons/plus.png')
    summary_btn_img = tk.PhotoImage(file='icons/menuList.png')

    # Clears window
    for i in master.winfo_children():
        i.destroy()

    if mode == 'main':
        add_task_lbl = tk.Label(text='Add new Task')
        add_task_lbl.pack(side='top', pady='25')
        add_btn = tk.Button(MAIN_WIND, command=lambda: create_screen(master, 'add_task'), image=addtask_btn_img)
        add_btn.pack(side='top')

        add_task_lbl = tk.Label(text='Goto Summary')
        add_task_lbl.pack(pady='25')
        summary_btn = tk.Button(MAIN_WIND, command=lambda: create_screen(master, 'open_summary'), image=summary_btn_img)
        summary_btn.pack()
    
    elif mode == 'add_task':

        back_btn = tk.Button(MAIN_WIND, text='Back', command=lambda: create_screen(master, 'main'), image=back_btn_img)
        back_btn.pack(anchor='w', padx='15', pady='15')

        spcfc_lbl = tk.Label(text='Goal * :\ne.g.: get better grades')
        spcfc_lbl.pack()
        spcfc_inp = tk.Entry()
        spcfc_inp.pack()

        meass_lbl = tk.Label(text='Way of Achieving the Goal:\ne.g.: Learning 1 Hour a Day')
        meass_lbl.pack()
        meass_inp = tk.Entry()
        meass_inp.pack()

        rwrd_lbl = tk.Label(text='Reward for Completion:\ne.g.: Good Grades')
        rwrd_lbl.pack()
        rwrd_inp = tk.Entry()
        rwrd_inp.pack()

        urg_scl = tk.Scale(label='Enter Urgency: ', orient='horizontal', from_=0, to=10)
        urg_scl.pack()

        imp_scl = tk.Scale(label='Enter Importance: ', orient='horizontal', from_=0, to=10)
        imp_scl.pack()

        confirm_btn = tk.Button(MAIN_WIND, text='confirm', image=confirm_btn_img,
                                command=lambda: [save_to_global_lst(EntryData(spcfc_inp.get(),
                                                                              meass_inp.get(), rwrd_inp.get(),
                                                                              imp_scl.get(), urg_scl.get())),
                                                 create_screen(master, 'main')])
        confirm_btn.pack(side='top', pady='25')
    
    elif mode == 'open_summary':
        back_btn = tk.Button(MAIN_WIND, command=lambda: create_screen(master, 'main'), image=back_btn_img)
        back_btn.pack(anchor='w', padx='15', pady='15')

        draw_hihi_btn = tk.Button(MAIN_WIND, text='(A) Do Now',
                                  command=lambda: create_screen(master, 'open_summary', 0, 'hihi'))
        draw_hihi_btn.pack(side='top')

        draw_hilo_btn = tk.Button(MAIN_WIND, text='(B) Do after A',
                                  command=lambda: create_screen(master, 'open_summary', 0, 'hilo'))
        draw_hilo_btn.pack()

        draw_lohi_btn = tk.Button(MAIN_WIND, text='(C) Plan for near Future',
                                  command=lambda: create_screen(master, 'open_summary', 0, 'lohi'))
        draw_lohi_btn.pack()

        draw_lolo_btn = tk.Button(MAIN_WIND, text='(D) Do when you have spare time',
                                  command=lambda: create_screen(master, 'open_summary', 0, 'lolo'))
        draw_lolo_btn.pack()

        spacer_lbl = tk.Label(MAIN_WIND)
        spacer_lbl.pack(pady='15')

        for i in ED_OBJ_LST:
            if i.quadrant == quadrant_to_draw:
                ed_obj_lbl = tk.Label(text=i.taskinfo)
                ed_obj_lbl.pack()
                x = tk.Button(MAIN_WIND, text='X', command=lambda i=i: create_screen(master, 'remove', i, i.quadrant))
                x.pack()

    elif mode == 'remove':
        ED_OBJ_LST.remove(obj_to_remove)
        create_screen(master, 'open_summary', 0, quadrant_to_draw)
    
    else:
        print('wrong mode chosen. going back to main.')
        create_screen(master, 'main')
    MAIN_WIND.mainloop()


# Create Main Window and Set Default Size and Title
MAIN_WIND = tk.Tk()
MAIN_WIND.geometry('500x500')
MAIN_WIND.minsize(500, 500)
MAIN_WIND.maxsize(500, 1080)
MAIN_WIND.title('Eisen Smart 1.0')
create_screen(MAIN_WIND, 'main')
