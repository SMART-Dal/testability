import seaborn as sns
import pandas as pd

rq3 = pd.read_csv('rq3_data_boxplot.csv')

sns.set_theme(style="whitegrid")
ax = sns.boxplot(x=rq3["Testability category"], y=rq3["Test density"], order=["C1(<5)", "C2(5-10)", "C3(10-20)", "C4(>20)"])
ax = sns.swarmplot(x=rq3["Testability category"], y=rq3["Test density"], color=".5", size=2, order=["C1(<5)", "C2(5-10)", "C3(10-20)", "C4(>20)"])

medians = rq3.groupby(['Testability category'])['Test density'].median()
vertical_offset = rq3['Test density'].median() * 0.05 # offset from median for display

for xtick in ax.get_xticks():
    ax.text(xtick, round(medians[xtick], 2) + vertical_offset,round(medians[xtick],2),
                  horizontalalignment='center',size='x-small',color='w',weight='semibold')
fig = ax.get_figure()
fig.savefig("rq3_boxplot.pdf")