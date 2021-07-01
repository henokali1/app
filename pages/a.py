import pickle

# with open('lc-log.pickle', 'wb') as handle:
#     pickle.dump([], handle, protocol=pickle.HIGHEST_PROTOCOL)


with open('lc-log.pickle', 'rb') as handle:
    old_val = pickle.load(handle)
print(old_val)