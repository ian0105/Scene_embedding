from src.function import *
from src.movie_class import *
from stellargraph.data import UniformRandomMetaPathWalk
from stellargraph import StellarGraph
from transformers import AutoTokenizer, AutoModel





def main(args):
    model = AutoModel.from_pretrained(args.model_path)
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    
    path = args.datg_path
    filenames = os.listdir(path)
    walk_length = 20  # maximum length of a random walk to use throughout this notebook


    metapaths = [
        ["act", "scene", "act"],
        ["act", "act", "scene", "act", "act"],
        ["act",'char', "act"],
        ["act", "act", "char", "act", "act"],
        ['char','act','scene','act','char'],
    ]
    for filename in filenames:
        mov = Movie(path+filename+'/script.txt')
        scene_embedding = scenesentence_to_embedding(mov.scene_dict)
        g = make_graph(scene_embedding)
        g = set_node(g)
        stellar_g = StellarGraph.from_networkx(g)
        stellar_g.info()
        rw = UniformRandomMetaPathWalk(stellar_g)
        walks1 = rw.run(
            nodes=list(stellar_g.nodes()),  # root nodes
            length=walk_length,  # maximum length of a random walk
            n=2,  # number of random walks per root node
            metapaths=metapaths,  # the metapaths
            )

        walks2 = rw.run(
            nodes=list(stellar_g.nodes()),  # root nodes
            length=walk_length*2,  # maximum length of a random walk
            n=60,  # number of random walks per root node
            metapaths=metapaths2,  # the metapaths
       )

        walks = []
        for w in walks1:
            walks.append(w)
        for w in walks2:
            walks.append(w)
    
        word2vec_train(g, filename, args.save_path, vector_size=384, window=5, min_count=0, sg=1, workers=4, epochs=60)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Preprocess movie scripts'
    )
    parser.add_argument('--data_path', default='../data/scriptbase/',
        help='Path to the long dialogue data', type=str)
        
    parser.add_argument('--model_path', default="sentence-transformers/multi-qa-MiniLM-L6-cos-v1",
        help='Path of SBERT', type=str)
    parser.add_argument('--save_path', default='word2vec_model',
        help='Path of SBERT', type=str)
           
    args = parser.parse_args()
    main(args)
