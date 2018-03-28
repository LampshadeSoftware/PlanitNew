def colors_generator(i=0):
	colors = ["#33B79B", "#CE5858", "#5869CE", "#BD4EAC"]
	while True:
		yield colors[i % len(colors)]
		i += 1

def get_perms(tup):
	if len(tup) == 1:
		yield (tup[0],)
	for i, val in enumerate(tup):
		for perm in get_perms(tup[:i] + tup[i+1:]):
			yield (val,) + perm

gen = colors_generator()
for i in range(10):
	print(next(gen))