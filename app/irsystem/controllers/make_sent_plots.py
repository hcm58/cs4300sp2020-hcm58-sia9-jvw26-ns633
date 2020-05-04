import matplotlib.pyplot as plt
import numpy as np

#helper function to plot the state's sentiment by day
def make_state_comment_plot(state, avg_by_day):
    lis = list(avg_by_day.items())
    lis.sort(key = lambda x: x[0])
    print(len(lis))

    if len(lis) < 2:
        return 'none'
    else:
        new_lis = []
        for tup in lis:
            month = tup[0][1]
            if month == "1":
                new_lis.append(tuple(("Jan " + str(tup[0][2:]), tup[1])))
            if month == "2":
                new_lis.append(tuple(("Feb " + str(tup[0][2:]), tup[1])))
            if month == "3":
                new_lis.append(tuple(("Mar " + str(tup[0][2:]), tup[1])))
            if month == "4":
                new_lis.append(tuple(("Apr " + str(tup[0][2:]), tup[1])))

        x_pos = np.arange(len(new_lis))
        labels = [x[0] for x in new_lis]

        fig = plt.figure(figsize=(9.0, 6.0))
        plt.bar(x_pos, [y[1] for y in new_lis])
        plt.xticks(x_pos, labels[::2], rotation='vertical') # set divisor
        plt.locator_params(axis='x', nbins=len(x_pos)/3)
        plt.gcf().subplots_adjust(bottom=0.20)
        # plt.xticks(plt.xticks(np.arange(x_lis[0], x_lis[len(x_lis)-1], 1.0)))
        # plt.xticks(rotation=70)
        plt.xlabel("Date")
        plt.ylabel("Avg Sentiment Score")
        plt.title("Average Comment Sentiment Score By Day")

        link = 'app/static/images/' + state + '_sent_plot1.png'

        fig.savefig(link)
        return 'plot'
