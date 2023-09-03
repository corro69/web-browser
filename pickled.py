import pickle

pickle_in = open("dweb_settings.dat","rb")
settings = pickle.load(pickle_in)
print(settings)
pickle_in.close()
