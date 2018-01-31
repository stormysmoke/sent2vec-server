from sent2vec.manager import Sent2VecManager

sent2vec = Sent2VecManager.get_instance()
sent2vec.load_model()
sent2vec.read_file("tmp_text.txt")
sent2vec.query("The church had multiple origins.", 3, "dist")
sent2vec.query("The church had multiple origins.", 3, "score")
