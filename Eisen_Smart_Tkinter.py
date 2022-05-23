import tkinter as tk
import pickle as pk
import os


class EntryData:
    # Specific, Measurable, Rewarding, Importance, Urgency
    def __init__(self, spcfc, meass, rewrd, impor, urgcy):
        self.spcfc = spcfc
        self.meass = meass
        self.rewrd = rewrd
        self.impor = impor
        self.urgcy = urgcy
        self.taskinfo = ''
        self.quadrant = ''

        #Creates string wich contains goal sentence
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

#Global List Containing all EntryData Objects which are added.
ED_OBJ_LST = []

def create_screen(master, mode, obj_to_remove=0, quadrant_to_draw=''):
    # icons originate from: https://www.kenney.nl/assets/game-icons
    back_btn_img = tk.PhotoImage(file='icons/arrowLeft.png')
    confirm_btn_img = tk.PhotoImage(file='icons/checkmark.png')
    addtask_btn_img = tk.PhotoImage(file='icons/plus.png')
    summary_btn_img = tk.PhotoImage(file='icons/menuList.png')
    save_btn_img = tk.PhotoImage(file='icons/save.png')
    load_btn_img = tk.PhotoImage(file='icons/target.png')

    #Used to Edit ED_OBJ_LST in this scope
    global ED_OBJ_LST

    # Clears all widgets of master window
    for i in master.winfo_children():
        i.destroy()

    if mode == 'main':
        add_task_lbl = tk.Label(text='Add new Task')
        add_task_lbl.pack(side='top', pady='20')
        add_btn = tk.Button(MAIN_WIND, command=lambda: create_screen(master, 'add_task'), image=addtask_btn_img)
        add_btn.pack(side='top')

        summary_lbl = tk.Label(text='Goto Summary')
        summary_lbl.pack(pady='20')
        summary_btn = tk.Button(MAIN_WIND, command=lambda: create_screen(master, 'open_summary'), image=summary_btn_img)
        summary_btn.pack()

        save_lbl = tk.Label(text='Save to txt')
        save_lbl.pack(pady='20')
        save_btn = tk.Button(MAIN_WIND, command=lambda: create_screen(master, 'save_to_txt'),image=save_btn_img)
        save_btn.pack()

        load_lbl = tk.Label(text='Load from txt')
        load_lbl.pack(pady='20')
        load_btn = tk.Button(MAIN_WIND, command=lambda: create_screen(master, 'load_from_txt'), image=load_btn_img)
        load_btn.pack()
    elif mode == 'save_to_txt':
        #uses pickle to save Global ED_OBJ_LST to file in saves/save.pkl
        out_file = open('saves/save.pkl','wb')
        pk.dump(ED_OBJ_LST,out_file)
        create_screen(master, 'main')

    elif mode == 'load_from_txt':
        #checks if .pkl file has content
        if os.path.getsize('saves/save.pkl') > 0:
            # uses pickle to initialize Global ED_OBJ_LST with objects of saves/save.pkl
            in_file = open('saves/save.pkl', 'rb')
            ED_OBJ_LST = pk.load(in_file)

        create_screen(master, 'main')

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

        #when confirm button is clicked. A new EntryData Object is Created and appended to Global ED_OBJ_LST
        confirm_btn = tk.Button(MAIN_WIND, text='confirm', image=confirm_btn_img,
                                command=lambda: [ED_OBJ_LST.append(EntryData(spcfc_inp.get(),meass_inp.get(),
                                                                   rwrd_inp.get(),imp_scl.get(),
                                                                   urg_scl.get())),create_screen(master, 'main')])
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

        #For space of one row
        spacer_lbl = tk.Label(MAIN_WIND)
        spacer_lbl.pack(pady='15')

        #checks every obj in ED_OBJ_LST. If Quadrant of Obj Equals Quadrant of create_screen parameter quadrant_to_draw draw obj
        for i in ED_OBJ_LST:
            if i.quadrant == quadrant_to_draw:
                ed_obj_lbl = tk.Label(text=i.taskinfo)
                ed_obj_lbl.pack()
                x = tk.Button(MAIN_WIND, text='X', command=lambda i=i: create_screen(master, 'remove', i, i.quadrant))
                x.pack()

    #removes obj_to_remove from global ED_OBJ_LST
    elif mode == 'remove':
        ED_OBJ_LST.remove(obj_to_remove)
        create_screen(master, 'open_summary', 0, quadrant_to_draw)

    #if no appropriate mode was chosen it's main
    else:
        print('wrong mode chosen. going back to main.')
        create_screen(master, 'main')
    MAIN_WIND.mainloop()


# Create Main Window and Set Default Size and Title
MAIN_WIND = tk.Tk()
MAIN_WIND.geometry('500x500')
MAIN_WIND.minsize(500, 500)
MAIN_WIND.maxsize(500, 1080)
MAIN_WIND.title('Eisen Smart')
create_screen(MAIN_WIND, 'main')
