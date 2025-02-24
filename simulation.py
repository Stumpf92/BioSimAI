import settings
import threading
import cProfile
import pstats

from agent import Agent
from game import Game
from display import Display
from terrain import Terrain
from plot import Plot

class Simulation:
    def __init__(self):
        self.n_counter = 0

        self.plot_scores = []    
        self.plot_mean_scores = []
        self.total_score = 0
        self.record = 0
        self.mean_score = 0

        self.terrain = Terrain()
        self.prey_agent = Agent(self)
        self.game = Game(self)        


        

    def train(self):
        
        all_valuable_informations = []
        
        if settings.DISPLAY_MODE:
            display = Display()
        if settings.PLOT_MODE:
            plot = Plot()
        
        self.game.reset()

        while self.n_counter < settings.MAX_GAMES_PER_SIMULATION:
            record_mode = False

            data_for_one_step = {}            

            frame_iteration, reward, game_over, score, map_per_tick, plant_count, prey_count= self.game.play_step()


            data_for_one_step["n_counter"] = self.n_counter        
            data_for_one_step["score"] = score
            data_for_one_step["frame_iteration"] = frame_iteration
            data_for_one_step["reward"] = reward
            data_for_one_step["game_over"] = game_over
            data_for_one_step["map_per_tick"] = map_per_tick.copy()
            data_for_one_step["plant_count"] = plant_count
            data_for_one_step["prey_count"] = prey_count
            # data_for_one_step["action"] = action
            data_for_one_step["terrain"] = self.terrain.terrain_map.copy()
            # data_for_one_step["action"] = final_move
            # data_for_one_step["state_old"] = state_old
            data_for_one_step["epsilon"] = self.prey_agent.epsilon
            

            if game_over:
                # train long memory, plot result
                self.game.reset()
                self.prey_agent.train_long_memory()
                
                self.plot_scores.append(score)
                self.total_score += score

                mean_score = self.total_score / (self.n_counter+1) if self.n_counter > 0 else 0
                self.plot_mean_scores.append(mean_score)

                if score > self.record:
                    self.record = score
                    record_mode = True

            
            data_for_one_step["record"] = self.record
            data_for_one_step["mean_score"] = self.mean_score
            data_for_one_step["record_mode"] = record_mode


            all_valuable_informations.append(data_for_one_step)


            if game_over and settings.DISPLAY_MODE:
                display.save(all_valuable_informations)
            
            if display.drawing_mode == False and len(display.queue_of_valuable_informations) > 0:
                threading.Thread(target=display.render).start()

            plot.save(self.n_counter, self.plot_scores, self.plot_mean_scores)  
            if game_over and settings.PLOT_MODE and (record_mode or self.n_counter % settings.PLOT_REDUCTION_FACTOR == 0):
                plot.update()
                pass



            if game_over:    
                print('Game', self.n_counter, 'Reward', score, 'Record:', self.record, 'Mean:', mean_score)
                self.n_counter += 1

                # reset the valuable informations to 0 for the next game
                all_valuable_informations = []

            


if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()

    simulation = Simulation()
    simulation.train()

    pr.disable()
    results = pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE)
    results.print_stats(50)
    # results.dump_stats("results.prof")