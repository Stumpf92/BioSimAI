import matplotlib.pyplot as plt
from IPython import display

class Plot:
    def __init__(self):   
        plt.ion()
        #mngr = plt.get_current_fig_manager()
        #mngr.window.setGeometry(50, 100, 640, 545)


    def save(self,n_games, plot_scores, plot_mean_scores):
        self.n_games = n_games
        self.plot_scores = plot_scores
        self.plot_mean_scores = plot_mean_scores

    def update(self):        
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games') 
        plt.plot(self.plot_scores)
        plt.plot(self.plot_mean_scores)
        plt.grid(True)
        plt.text(len(self.plot_scores)-1, self.plot_scores[-1], str(self.plot_scores[-1]))
        plt.text(len(self.plot_mean_scores)-1, self.plot_mean_scores[-1], str(self.plot_mean_scores[-1]))
        plt.show(block=False)
        plt.pause(.5)
        pass

    def end(self):
        plt.close()



if __name__ == "__main__":
    exec(open("agent.py").read())