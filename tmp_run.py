from sent2vec.manager import Sent2VecManager

sent2vec = Sent2VecManager.get_instance()

print("Loading model:")
sent2vec.load_model()

print("Indexing sample text...")
sent2vec.read_file("tmp_text.txt")

print("Result of sample 'dist' query:")
l = sent2vec.query("The church had multiple origins.", 3, "dist")
print(l)

print("Result of sample 'score' query:")
l = sent2vec.query("The church had multiple origins.", 3, "dist")
l = sent2vec.query("The church had multiple origins.", 3, "score")
print(l)
