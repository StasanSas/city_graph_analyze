from my_code.code.algos.statistics.read_and_save import save, load
s = load('Ну, базовая статистика')
print(s.config)
print(s.mean_statistic.get_mean() // 60)
print(s.statistic_percentile.get_percentile(0.25) // 60)
print(s.statistic_percentile.get_percentile(0.5) // 60)
print(s.statistic_percentile.get_percentile(0.75) // 60)
print(s.statistic_percentile.get_percentile(0.95) // 60)

for node in s.statistic_means_for_nodes.d_means_count.keys():
    print(s.statistic_means_for_nodes.get_mean(node))