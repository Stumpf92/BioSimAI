import settings
# from plant import Plant
# from prey import Prey
# from hunter import Hunter
from creature import Plant, Prey, Hunter
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import numpy as np
import time


class Display:
    def __init__(self, app):
        self.app = app
        self.n_game_counter = 0
        self.n_tick_counter = 0
        self.cur_all_data_length = 0

        self.start = time.time()
        self.starting_fps = settings.FPS
        self.pause_mode = False
        self.latest_mode = False

        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue") 

        self.root = ctk.CTk()  
        self.root.title("BioSim")

        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=1)
        self.root.columnconfigure(2,weight=1)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)


        # TOP LEFT

        self.top_left_frame = ctk.CTkFrame(self.root)
        self.top_left_frame.grid(column=0, row= 0, sticky= "n")

        fig1 = Figure( dpi=100, frameon=True)
        fig1.set_size_inches(settings.DIAGRAM_WIDTH,settings.DIAGRAM_HEIGHT)
        self.graph1 = fig1.add_subplot(1,1,1)
        self.diagram1 = FigureCanvasTkAgg(fig1, master=self.top_left_frame)
        self.diagram1.get_tk_widget().pack(padx = 15 , pady= 15)

        fig4 = Figure( dpi=100, frameon=True)
        fig4.set_size_inches(settings.DIAGRAM_WIDTH,settings.DIAGRAM_HEIGHT)
        self.graph4 = fig4.add_subplot(1,1,1)
        self.diagram4 = FigureCanvasTkAgg(fig4, master=self.top_left_frame)
        self.diagram4.get_tk_widget().pack(padx = 15 , pady= 15)

        fig5 = Figure( dpi=100, frameon=True)
        fig5.set_size_inches(settings.DIAGRAM_WIDTH,settings.DIAGRAM_HEIGHT)
        self.graph5 = fig5.add_subplot(1,1,1)
        self.diagram5 = FigureCanvasTkAgg(fig5, master=self.top_left_frame)
        self.diagram5.get_tk_widget().pack(padx = 15 , pady= 15)

        
        # BOT LEFT
        

        self.bot_left_frame = ctk.CTkFrame(self.root)
        self.bot_left_frame.grid(column=0, row= 1, sticky= "n")

        self.bot_left_frame1 = ctk.CTkFrame(self.bot_left_frame)
        self.bot_left_frame1.pack(padx = 15, pady= 15 )

        self.record_mode_switch = ctk.CTkSwitch(master=self.bot_left_frame1, text="latest mode", command=self.set_latest_mode, height=29)
        self.record_mode_switch.pack(padx = 15 )

        self.bot_left_frame2 = ctk.CTkFrame(self.bot_left_frame)
        self.bot_left_frame2.pack(padx = 15 , pady= 15)

        far_backward_game_button = ctk.CTkButton(master=self.bot_left_frame2,text="<<--",command=self.far_backward_game, width = 45)
        far_backward_game_button.pack(padx = 15 , side= "left")

        far_forward_game_button = ctk.CTkButton(master=self.bot_left_frame2,text="-->>",command=self.far_forward_game, width = 45)
        far_forward_game_button.pack(padx = 15 , side="right")

        forward_game_button = ctk.CTkButton(master=self.bot_left_frame2,text="-->",command=self.forward_game, width = 45)
        forward_game_button.pack(padx = 15 , side= "right")

        backward_game_button = ctk.CTkButton(master=self.bot_left_frame2,text="<--",command=self.backward_game, width = 45)
        backward_game_button.pack(padx = 15 , side="right")







        # TOP MIDDLE
        
        
        self.top_middle_frame = ctk.CTkFrame(self.root)
        self.top_middle_frame.grid(column=1, row= 0, sticky= "n")

        self.mode_slider = ctk.CTkSlider(master=self.top_middle_frame, from_=0, to=2, number_of_steps=2, command=self.set_mode, height=29)
        self.mode_slider.pack(padx = 15 , pady= 15)

        self.label_time = ctk.CTkLabel(self.top_middle_frame, text="")
        self.label_time.pack(padx = 15 , pady= 1)

        self.label_game_counter = ctk.CTkLabel(self.top_middle_frame, text="")
        self.label_game_counter.pack(padx = 15 , pady= 1)

        self.label_tick_counter = ctk.CTkLabel(self.top_middle_frame, text="")
        self.label_tick_counter.pack(padx = 15 , pady= 1)

        self.box = ctk.CTkCanvas(self.top_middle_frame, width=settings.GRID_WIDTH*settings.GRID_SIZE, height=settings.GRID_HEIGHT*settings.GRID_SIZE)
        self.box.pack(padx = 15 , pady= 15, side = "bottom")

        
        # BOT MIDDLE

        self.bot_middle_frame = ctk.CTkFrame(self.root)
        self.bot_middle_frame.grid(column=1, row= 1, sticky= "n")
        
        reset_button = ctk.CTkButton(master=self.bot_middle_frame,text="reset",command=self.reset)
        reset_button.grid(padx = 15 , pady= 15, column=0, row= 1,)

        save_button = ctk.CTkButton(master=self.bot_middle_frame,text="save",command=self.save)
        save_button.grid(padx = 15 , pady= 15, column=1, row= 0,)

        load_button = ctk.CTkButton(master=self.bot_middle_frame,text="load",command=self.load)
        load_button.grid(padx = 15 , pady= 15, column=0, row= 0,)

        quit_button = ctk.CTkButton(master=self.bot_middle_frame,text="quit",command=self.display_quit)
        quit_button.grid(padx = 15 , pady= 15, column=1, row= 1,)

        


        # TOP RIGHT

        self.top_right_frame = ctk.CTkFrame(self.root)
        self.top_right_frame.grid(column=2, row= 0, sticky= "n")



        fig2 = Figure( dpi=100, frameon=True)
        fig2.set_size_inches(settings.DIAGRAM_WIDTH,settings.DIAGRAM_HEIGHT)
        self.graph2 = fig2.add_subplot(1,1,1)
        self.diagram2 = FigureCanvasTkAgg(fig2, master=self.top_right_frame)
        self.diagram2.get_tk_widget().pack(padx = 15 , pady= 15)

        fig3 = Figure( dpi=100, frameon=True)
        fig3.set_size_inches(settings.DIAGRAM_WIDTH,settings.DIAGRAM_HEIGHT)
        self.graph3 = fig3.add_subplot(1,1,1)
        self.diagram3 = FigureCanvasTkAgg(fig3, master=self.top_right_frame)
        self.diagram3.get_tk_widget().pack(padx = 15 , pady= 15)

        fig6 = Figure( dpi=100, frameon=True)
        fig6.set_size_inches(settings.DIAGRAM_WIDTH,settings.DIAGRAM_HEIGHT)
        self.graph6 = fig6.add_subplot(1,1,1)
        self.diagram6 = FigureCanvasTkAgg(fig6, master=self.top_right_frame)
        self.diagram6.get_tk_widget().pack(padx = 15 , pady= 15)



        # BOT RIGHT

        self.bot_right_frame = ctk.CTkFrame(self.root)
        self.bot_right_frame.grid(column=2, row= 1, sticky= "n")

        self.bot_right_frame1 = ctk.CTkFrame(self.bot_right_frame)
        self.bot_right_frame1.pack(padx = 15 , pady= 15)

        self.bot_right_frame2 = ctk.CTkFrame(self.bot_right_frame)
        self.bot_right_frame2.pack(padx = 15 , pady= 15)




        self.slider = ctk.CTkSlider(master=self.bot_right_frame1, from_=1, to=100, number_of_steps=100, command=self.update_slider, height=29)
        self.slider.pack(padx = 15 )

        far_backward_tick_button = ctk.CTkButton(master=self.bot_right_frame2,text="<<--",command=self.far_backward_tick, width = 45)
        far_backward_tick_button.pack(padx = 15, side= "left")

        far_forward_tick_button = ctk.CTkButton(master=self.bot_right_frame2,text="-->>",command=self.far_forward_tick, width = 45)
        far_forward_tick_button.pack(padx = 15, side="right")

        forward_tick_button = ctk.CTkButton(master=self.bot_right_frame2,text="-->",command=self.forward_tick, width = 45)
        forward_tick_button.pack(padx = 15, side= "right")

        backward_tick_button = ctk.CTkButton(master=self.bot_right_frame2,text="<--",command=self.backward_tick, width = 45)
        backward_tick_button.pack(padx = 15, side="right")


        self.counter = 0
        

        self.update()        
        self.root.mainloop()

    def set_mode(self, value):
        if value == 0:
            self.app.display_mode = False
            self.app.simulation_mode = True
        elif value == 1:
            self.app.simulation_mode = True
            self.app.display_mode = True
            # self.update()

        elif value == 2:
            self.app.simulation_mode = False
            self.app.display_mode = True


    def set_latest_mode(self):
        self.latest_mode = not self.latest_mode

    def load(self):
        self.app.simulation.prey_agent.model.load()

    def save(self):
        self.app.simulation.prey_agent.model.save()
    
    def update_slider(self, value):
        self.starting_fps = value
          
    
    def display_quit(self): 
        # Simulationsthread und Mainthread(Display) beenden
        self.app.simulation.running = False    
        self.root.destroy()

    def far_backward_game(self):
        self.n_game_counter = max(self.n_game_counter-10,0)
        self.n_tick_counter= 0
        self.update_new_game_data()

    def backward_game(self):
        self.n_game_counter = max(self.n_game_counter-1,0)
        self.n_tick_counter= 0
        self.update_new_game_data()

    def forward_game(self):
        self.n_game_counter = min(self.n_game_counter+1,self.n_game_counter_array[-1])
        self.n_tick_counter= 0
        self.update_new_game_data()

    def far_forward_game(self):
        self.n_game_counter = min(self.n_game_counter+10,self.n_game_counter_array[-1])
        self.n_tick_counter= 0
        self.update_new_game_data()
        
    def far_backward_tick(self):
        self.n_tick_counter = max(self.n_tick_counter-10,0)
        
    def backward_tick(self):
        self.n_tick_counter = max(self.n_tick_counter-1,0)
    
    def pause_display_tick(self):
        self.pause_mode = bool(int(self.pause_mode)-1)
        if self.pause_mode:
            self.pause_display_button.configure(text = ">>")
        else:
            self.pause_display_button.configure(text = "||")

    def forward_tick(self):
        self.n_tick_counter = min(self.n_tick_counter+1,settings.MAX_TICKS_PER_GAME-1)
        
    def far_forward_tick(self):
        self.n_tick_counter = min(self.n_tick_counter+10,settings.MAX_TICKS_PER_GAME-1)
                


    def update(self):
        self.update_once_per_sim()
        def my_after():
            if self.app.display_mode:
                self.update_every_tick()
            else:
                time.sleep(0.1)
            
            self.root.after(int(1000/self.starting_fps), my_after)
        my_after()    


    def update_once_per_sim(self):
        pass


    def update_new_game_data(self):

        # draw graphs when new game data is ready        

        self.n_game_counter_array = []
        self.cum_end_reward_array = []
        self.mean_cum_end_reward_array = []
        self.positive_record_array = []
        self.negative_record_array = []
        self.prey_epsilon_end_of_game_array = []
        self.hunter_epsilon_end_of_game_array = []
        self.calc_duration_array = []


        for i in self.app.all_data:
            self.n_game_counter_array.append(i["n_game_counter"])
            self.cum_end_reward_array.append(i["cum_end_reward"])
            self.mean_cum_end_reward_array.append(i["mean_cum_end_reward"])
            self.positive_record_array.append(i["positive_record"])
            self.negative_record_array.append(i["negative_record"])
            self.prey_epsilon_end_of_game_array.append(i["prey_epsilon_end_of_game"])
            self.hunter_epsilon_end_of_game_array.append(i["hunter_epsilon_end_of_game"])
            self.calc_duration_array.append(i["calc_duration"])
        
        self.n_game_counter_array = np.array(self.n_game_counter_array)
        self.cum_end_reward_array = np.array(self.cum_end_reward_array)
        self.mean_cum_end_reward_array = np.array(self.mean_cum_end_reward_array)
        self.positive_record_array = np.array(self.positive_record_array)
        self.negative_record_array = np.array(self.negative_record_array)
        self.prey_epsilon_end_of_game_array = np.array(self.prey_epsilon_end_of_game_array)
        self.hunter_epsilon_end_of_game_array = np.array(self.hunter_epsilon_end_of_game_array)
        self.calc_duration_array = np.array(self.calc_duration_array)




        #  left graph from top to bottom

        self.graph1.clear()        
        self.graph1.set_title("cum_reward and mean per game")
        self.graph1.grid(True)
        self.graph1.plot(self.n_game_counter_array, self.cum_end_reward_array, 'c', linewidth=1)
        self.graph1.plot(self.n_game_counter_array, self.mean_cum_end_reward_array, 'm', linewidth=1)
        self.graph1.plot(self.n_game_counter_array, self.positive_record_array, 'g', linewidth=1)
        self.graph1.plot(self.n_game_counter_array, self.negative_record_array, 'r', linewidth=1)
        self.graph1.axvline(x=self.n_game_counter, color='r', linestyle='dashed', linewidth=1)
        self.diagram1.draw()

        self.graph4.clear()        
        self.graph4.set_title("epsilon per game")
        self.graph4.grid(True)
        self.graph4.plot(self.n_game_counter_array, self.prey_epsilon_end_of_game_array, 'g', linewidth=1)     
        self.graph4.plot(self.n_game_counter_array, self.hunter_epsilon_end_of_game_array, 'r', linewidth=1)   
        self.graph4.axvline(x=self.n_game_counter, color='r', linestyle='dashed', linewidth=1)
        self.diagram4.draw() 

        self.graph5.clear()        
        self.graph5.set_title("duration per game in s")
        self.graph5.grid(True)
        self.graph5.plot(self.n_game_counter_array, self.calc_duration_array, 'c', linewidth=1)   
        self.graph5.axvline(x=self.n_game_counter, color='r', linestyle='dashed', linewidth=1)
        self.diagram5.draw()       

        # update graphs to the right

        self.n_tick_counter_array = []
        self.plant_count_array = []
        self.prey_count_array = []
        self.hunter_count_array = []
        self.reward_array = []
        self.cum_reward_array = []

        max_tick_counter_for_this_game = self.app.all_data[self.n_game_counter]["info_per_tick"][-1]["n_tick_counter"]

        for i in range(max_tick_counter_for_this_game):
            self.n_tick_counter_array.append(self.app.all_data[self.n_game_counter]["info_per_tick"][i]["n_tick_counter"])
            self.plant_count_array.append(self.app.all_data[self.n_game_counter]["info_per_tick"][i]["plant_count"])
            self.prey_count_array.append(self.app.all_data[self.n_game_counter]["info_per_tick"][i]["prey_count"])
            self.hunter_count_array.append(self.app.all_data[self.n_game_counter]["info_per_tick"][i]["hunter_count"])
            self.reward_array.append(self.app.all_data[self.n_game_counter]["info_per_tick"][i]["reward"])
            self.cum_reward_array.append(self.app.all_data[self.n_game_counter]["info_per_tick"][i]["cum_reward"])


        self.n_tick_counter_array = np.array(self.n_tick_counter_array)
        self.plant_count_array = np.array(self.plant_count_array)
        self.prey_count_array = np.array(self.prey_count_array)
        self.hunter_count_array = np.array(self.hunter_count_array)
        self.reward_array = np.array(self.reward_array)
        self.cum_reward_array = np.array(self.cum_reward_array)
        
        # update box, draw background terrain
        for i in self.box.find_withtag("delete_every_game"):
            self.box.delete(i)
        if self.app.all_data:
            terrain = self.app.all_data[0]["terrain"]

            for x in range(settings.GRID_WIDTH):
                for y in range(settings.GRID_HEIGHT):
                    color = (int(settings.TERRAIN_BASE_COLOR[0]+terrain[x,y]*settings.TERRAIN_COLOR_STEP),
                            int(settings.TERRAIN_BASE_COLOR[1]+terrain[x,y]*settings.TERRAIN_COLOR_STEP),
                                int(settings.TERRAIN_BASE_COLOR[2]+terrain[x,y]*settings.TERRAIN_COLOR_STEP))
                    self.box.create_rectangle(x*settings.GRID_SIZE,
                                               y*settings.GRID_SIZE,
                                                 x*settings.GRID_SIZE+settings.GRID_SIZE,
                                                   y*settings.GRID_SIZE+settings.GRID_SIZE,
                                                     fill=self._from_rgb(color),
                                                       tags="delete_every_game",
                                                       width=0)

        self.graph2.clear() 
        self.graph2.set_title("plant and prey count, game: "+ str(self.n_game_counter))
        self.graph2.grid(True)
        self.graph2.plot(self.n_tick_counter_array, self.plant_count_array, 'g', linewidth=1)
        self.graph2.plot(self.n_tick_counter_array, self.prey_count_array, 'b', linewidth=1)
        self.graph2.plot(self.n_tick_counter_array, self.hunter_count_array, 'r', linewidth=1)
        self.graph2_axvline = self.graph2.axvline(x=self.n_tick_counter, color='m', linestyle='dashed', linewidth=1)

        self.graph3.clear()        
        self.graph3.set_title("reward, game: "+ str(self.n_game_counter))
        self.graph3.grid(True)
        self.graph3.plot(self.n_tick_counter_array, self.reward_array, 'c', linewidth=1)
        self.graph3_axvline = self.graph3.axvline(x=self.n_tick_counter, color='m', linestyle='dashed', linewidth=1)

        self.graph6.clear()        
        self.graph6.set_title("cum reward, game: "+ str(self.n_game_counter))
        self.graph6.grid(True)
        self.graph6.plot(self.n_tick_counter_array, self.cum_reward_array, 'c', linewidth=1)
        self.graph6_axvline = self.graph6.axvline(x=self.n_tick_counter, color='m', linestyle='dashed', linewidth=1)



    def update_every_tick(self):
        if self.app.all_data:
            #check if new data in all_data
            if self.cur_all_data_length < len(self.app.all_data):
                self.update_new_game_data()
                self.cur_all_data_length = len(self.app.all_data)
            
            
            # update timer
            self.label_time.configure(text="Simulationsdauer: " + str(round(time.time() - self.start,2))+ " s")
            self.label_game_counter.configure(text="Game: " + str(self.n_game_counter)+ "/"+ str(len(self.app.all_data)-1))
            self.label_tick_counter.configure(text="Tick: " + str(self.n_tick_counter)+ "/"+ str(settings.MAX_TICKS_PER_GAME-1))
            
            
            
            self.graph2_axvline.remove()
            self.graph2_axvline = self.graph2.axvline(x=self.n_tick_counter, color='m', linestyle='dashed', linewidth=1)
            self.diagram2.draw()

            self.graph3_axvline.remove()
            self.graph3_axvline = self.graph3.axvline(x=self.n_tick_counter, color='m', linestyle='dashed', linewidth=1)
            self.diagram3.draw()

            self.graph6_axvline.remove()
            self.graph6_axvline = self.graph6.axvline(x=self.n_tick_counter, color='m', linestyle='dashed', linewidth=1)
            self.diagram6.draw()

            for i in self.box.find_withtag("delete_every_tick"):
                self.box.delete(i)
            for x in range(settings.GRID_WIDTH):
                for y in range(settings.GRID_HEIGHT):
                    if isinstance(self.app.all_data[self.n_game_counter]["info_per_tick"][self.n_tick_counter]["map_per_tick"][x,y], Plant):
                        body = self.app.all_data[self.n_game_counter]["info_per_tick"][self.n_tick_counter]["map_per_tick"][x,y]
                        self.box.create_aa_circle(x*settings.GRID_SIZE+ settings.GRID_SIZE//2,
                                                        y*settings.GRID_SIZE+ settings.GRID_SIZE//2,
                                                        max(settings.GRID_SIZE//4,int((body.hp/body.heritage_stats["max_hp"]) *(settings.GRID_SIZE//2))),
                                                        fill=self._from_rgb((0,255,0)),
                                                        tags=("delete_every_tick"))
                    elif isinstance(self.app.all_data[self.n_game_counter]["info_per_tick"][self.n_tick_counter]["map_per_tick"][x,y], Prey):
                        body = self.app.all_data[self.n_game_counter]["info_per_tick"][self.n_tick_counter]["map_per_tick"][x,y]
                        self.box.create_aa_circle(x*settings.GRID_SIZE+ settings.GRID_SIZE//2,
                                                        y*settings.GRID_SIZE+ settings.GRID_SIZE//2,
                                                        max(settings.GRID_SIZE//4,int((body.hp/body.heritage_stats["max_hp"]) *(settings.GRID_SIZE//2))),
                                                        fill=self._from_rgb((0,0,255)),
                                                        tags=("delete_every_tick"))
                    elif isinstance(self.app.all_data[self.n_game_counter]["info_per_tick"][self.n_tick_counter]["map_per_tick"][x,y], Hunter):
                        body = self.app.all_data[self.n_game_counter]["info_per_tick"][self.n_tick_counter]["map_per_tick"][x,y]
                        self.box.create_aa_circle(x*settings.GRID_SIZE+ settings.GRID_SIZE//2,
                                                        y*settings.GRID_SIZE+ settings.GRID_SIZE//2,
                                                        max(settings.GRID_SIZE//4,int((body.hp/body.heritage_stats["max_hp"]) *(settings.GRID_SIZE//2))),
                                                        fill=self._from_rgb((255,0,0)),
                                                        tags=("delete_every_tick"))
            


            # increase n_tick_counter and eventual increase n_game_counter
            if self.pause_mode == False:
                self.n_tick_counter += 1
            
            max_tick_counter_for_this_game = self.app.all_data[self.n_game_counter]["info_per_tick"][-1]["n_tick_counter"]

            if self.n_tick_counter >= max_tick_counter_for_this_game:
                if self.latest_mode:
                    self.n_game_counter = len(self.app.all_data)-1
                else:
                    self.n_game_counter = min(self.n_game_counter+1,self.n_game_counter_array[-1])
                self.update_new_game_data()
                self.n_tick_counter = 0
        

    def _from_rgb(self, rgb):
      r, g, b = rgb
      return f'#{r:02x}{g:02x}{b:02x}'

    def reset(self):
        print("reset")


if __name__ == "__main__":
    exec(open("main.py").read())
