import pandas as pd
from aphylogeo.alignement import AlignSequences
from aphylogeo.params import Params
from aphylogeo import utils
from aphylogeo.genetic_trees import GeneticTrees

# from aphylogeo.utils import climaticPipeline, geneticPipeline, filterResults, loadSequenceFile

titleCard = r"""
        ____    __               ___           ____
       /\  _`\ /\ \             /\_ \         /\  _`\
   __  \ \ \L\ \ \ \___   __  __\//\ \     ___\ \ \L\_\     __    ___
 /'__`\ \ \ ,__/\ \  _ `\/\ \/\ \ \ \ \   / __`\ \ \L_L   /'__`\ / __`\
/\ \L\.\_\ \ \/  \ \ \ \ \ \ \_\ \ \_\ \_/\ \L\ \ \ \/, \/\  __//\ \L\ \
\ \__/.\_\\ \_\   \ \_\ \_\/`____ \/\____\ \____/\ \____/\ \____\ \____/
 \/__/\/_/ \/_/    \/_/\/_/`/___/> \/____/\/___/  \/___/  \/____/\/___/
                              /\___/
                              \/__/
"""  # https://patorjk.com/software/taag/#p=display&f=Larry%203D&t=aphylogeo%20

if __name__ == "__main__":
    print(titleCard + "\n")

    # load GeneticTrees from json
    # Params.UpdateParams(params_content={"rate_similarity": 322})
    # geneticTrees = GeneticTrees.load_trees_from_file("./debug/geneticTreesTest.json")
    # Phylo.write(tree1, "data/tree1.nwk", "newick")
    # seq_alignment.save_to_json("./debug/sequences_aligned.json")
    # loaded_seq_alignment = Alignment.load_from_json("./debug/sequences_aligned.json")

    Params.load_config_from_file()
    sequenceFile = utils.loadSequenceFile(Params.reference_gene_filepath)
    seq_alignment = AlignSequences(sequenceFile).align()

    geneticTrees = utils.geneticPipeline(seq_alignment.msa)
    trees = GeneticTrees(trees_dict=geneticTrees, format="newick")
    # trees.save_trees_to_json("./debug/geneticTreesTest.json")

    df = pd.read_csv(Params.file_name)
    climaticTrees = utils.climaticPipeline(df)
    utils.filterResults(climaticTrees, geneticTrees, df)
