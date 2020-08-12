import matplotlib.pyplot as plt
import pandas as pd


class Graph(object):

    def create_graph(self):
        plt.style.use('classic')
        results = pd.read_csv('records.csv', index_col=0)
        x1 = results.index
        y1 = results['zombies'] / (results['heroes'] + results['zombies'])
        plt.plot(x1, y1, label="line 1")
        plt.xlabel('Time (S)')
        plt.ylabel("Infected")
        plt.savefig('Figure_1.png')

# if __name__ == '__main__':
#     results = pd.read_csv('records.csv', index_col=0)
#     x1 = results.index
#     y1 = results['zombies']/(results['heroes']+results['zombies'])
#     plt.plot(x1, y1, label="line 1")
#     plt.xlabel('x - axis')
#     plt.show()
#     # os.remove('Figure_1.png')
#     # plt.savefig('Figure_1.png')
