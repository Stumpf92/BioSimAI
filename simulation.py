import settings
import threading
import time
import sys

from agent import Agent
from game import Game
from terrain import Terrain



class Simulation:
    def __init__(self, app):
        self.app = app

        self.n_game_counter = 0

        self.prey_total_score = 0
        self.hunter_total_score = 0
        self.prey_positive_record = 0
        self.hunter_positive_record = 0

        
        self.record_mode = False

        self.terrain = Terrain()
        self.prey_agent = Agent(self)
        self.hunter_agent = Agent(self)
        self.game = Game(self)

        self.running = True

    def train(self):

        self.game.reset() ####!
        info_per_tick = []  



        while self.n_game_counter < settings.MAX_GAMES_PER_SIMULATION and self.running == True:
            while self.app.simulation_mode == False and self.running == True:
                time.sleep(1)     
            start = time.time()
            self.record_mode = False    
              

            n_tick_counter, plantmap_per_tick, preymap_per_tick, huntermap_per_tick, seedmap_per_tick, plant_count, prey_count, hunter_count, seed_count, prey_reward, prey_cum_reward, hunter_reward, hunter_cum_reward, game_over = self.game.play_step()

            info_per_tick.append({"n_tick_counter": n_tick_counter,
                                  "plantmap_per_tick": plantmap_per_tick.copy(),
                                  "preymap_per_tick": preymap_per_tick.copy(),
                                  "huntermap_per_tick": huntermap_per_tick.copy(),
                                  "seedmap_per_tick": seedmap_per_tick.copy(),
                                  "plant_count": plant_count,
                                  "prey_count": prey_count,
                                  "hunter_count": hunter_count,
                                  "seed_count" : seed_count,
                                  "prey_reward" : prey_reward,
                                  "prey_cum_reward": prey_cum_reward,
                                  "hunter_reward": hunter_reward,
                                  "hunter_cum_reward": hunter_cum_reward,})
            if game_over:
                # train long memory, plot result
                self.game.reset()
                if settings.PREY_COUNT_START > 0:
                    self.prey_agent.train_long_memory()
                if settings.HUNTER_COUNT_START > 0:
                    self.hunter_agent.train_long_memory()
                
                self.prey_total_score += prey_cum_reward
                self.hunter_total_score += hunter_cum_reward

                prey_mean_cum_end_reward = self.prey_total_score / (self.n_game_counter+1) if self.n_game_counter > 0 else 0
                hunter_mean_cum_end_reward = self.hunter_total_score / (self.n_game_counter+1) if self.n_game_counter > 0 else 0

                if prey_cum_reward > self.prey_positive_record:
                    self.prey_positive_record = prey_cum_reward
                    self.record_mode = True
                if hunter_cum_reward > self.hunter_positive_record:
                    self.hunter_positive_record = hunter_cum_reward
                    self.record_mode = True


                info_per_game = {}

                info_per_game["n_game_counter"] = self.n_game_counter
                info_per_game["prey_cum_end_reward"] = prey_cum_reward
                info_per_game["prey_mean_cum_end_reward"] = prey_mean_cum_end_reward
                info_per_game["prey_positive_record"] = self.prey_positive_record                
                info_per_game["prey_epsilon_end_of_game"] = self.prey_agent.epsilon  
                info_per_game["hunter_cum_end_reward"] = hunter_cum_reward
                info_per_game["hunter_mean_cum_end_reward"] = hunter_mean_cum_end_reward
                info_per_game["hunter_positive_record"] = self.hunter_positive_record
                info_per_game["hunter_epsilon_end_of_game"] = self.hunter_agent.epsilon

                info_per_game["terrain"] = self.terrain.terrain_map.copy()
                info_per_game["info_per_tick"] = info_per_tick.copy()
                info_per_game["calc_duration"] = (time.time() - start)

                self.app.all_data.append(info_per_game)

                print(f"Game {self.n_game_counter} finished")

                info_per_tick = []  
                self.n_game_counter += 1


            


if __name__ == "__main__":
    exec(open("main.py").read())
