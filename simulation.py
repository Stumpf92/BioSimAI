import settings
import threading
import time

from agent import Agent
from game import Game
from display import Display
from terrain import Terrain



class Simulation:
    def __init__(self, app):
        self.app = app

        self.n_game_counter = 0

        self.total_score = 0
        self.record_mode = False
        self.positive_record = 0
        self.negative_distance_to_mean = 0
        self.negative_record = 0
        self.mean_score = 0

        self.terrain = Terrain()
        self.prey_agent = Agent(self)
        self.game = Game(self)

        self.running = True

    def train(self):

        self.game.reset() ####!
        info_per_tick = []  

        while self.n_game_counter < settings.MAX_GAMES_PER_SIMULATION and self.running == True:
            start = time.time()       

            self.record_mode = False           
              

            n_tick_counter, map_per_tick, plant_count, prey_count, reward, cum_reward, game_over = self.game.play_step()

            info_per_tick.append({"n_tick_counter": n_tick_counter,
                                  "map_per_tick": map_per_tick.copy(),
                                  "plant_count": plant_count,
                                  "prey_count": prey_count,
                                  "reward" : reward,
                                  "cum_reward": cum_reward})
            if game_over:
                # train long memory, plot result
                self.game.reset()
                self.prey_agent.train_long_memory()
                
                self.total_score += cum_reward

                mean_cum_end_reward = self.total_score / (self.n_game_counter+1) if self.n_game_counter > 0 else 0
                #self.plot_mean_scores.append(mean_score)

                if cum_reward > self.positive_record:
                    self.positive_record = cum_reward
                    self.record_mode = True

                if (mean_cum_end_reward-cum_reward) > self.negative_distance_to_mean:
                    self.negative_distance_to_mean = mean_cum_end_reward-cum_reward
                    self.negative_record = cum_reward
                    self.record_mode = True

                info_per_game = {}
                info_per_game["n_game_counter"] = self.n_game_counter
                info_per_game["cum_end_reward"] = cum_reward
                info_per_game["mean_cum_end_reward"] = mean_cum_end_reward
                info_per_game["record_mode"] = self.record_mode
                info_per_game["positive_record"] = self.positive_record
                info_per_game["negative_record"] = self.negative_record
                info_per_game["terrain"] = self.terrain.terrain_map.copy()
                info_per_game["info_per_tick"] = info_per_tick.copy()
                info_per_game["epsilon_end_of_game"] = self.prey_agent.epsilon
                info_per_game["calc_duration"] = (time.time() - start)

                self.app.all_data.append(info_per_game)

                print('Game', self.n_game_counter, 'Reward', cum_reward, 'Record:', self.positive_record, 'Mean:', mean_cum_end_reward)

                info_per_tick = []  
                self.n_game_counter += 1


            


if __name__ == "__main__":
    exec(open("main.py").read())
